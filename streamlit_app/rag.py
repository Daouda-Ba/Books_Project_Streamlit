"""Page RAG - Assistant avec recherche semantique et LLM."""

import os
from pathlib import Path
from typing import Optional

import faiss
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from sentence_transformers import SentenceTransformer

from utils.data_loader import load_rag_data
from utils.logger import get_logger
from utils.validators import validate_dataframe

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)
logger = get_logger(__name__)

st.set_page_config(page_title="Mauribooks - AI Assistant", layout="wide")


def get_secret_value(name: str) -> Optional[str]:
    """Lit un secret Streamlit s'il est disponible."""
    try:
        value = st.secrets.get(name)
    except Exception:
        return None
    return str(value) if value else None


def get_hf_config() -> tuple[Optional[str], str, str]:
    """Retourne le token HF, le modele et la source du token."""
    env_api_key = os.getenv("HF_API_KEY")
    env_token = os.getenv("HF_TOKEN")
    secret_api_key = get_secret_value("HF_API_KEY")
    secret_token = get_secret_value("HF_TOKEN")

    if env_api_key:
        token = env_api_key
        source = "HF_API_KEY (.env ou variable d'environnement)"
    elif env_token:
        token = env_token
        source = "HF_TOKEN (.env ou variable d'environnement)"
    elif secret_api_key:
        token = secret_api_key
        source = "HF_API_KEY (Streamlit secrets)"
    elif secret_token:
        token = secret_token
        source = "HF_TOKEN (Streamlit secrets)"
    else:
        token = None
        source = "aucun token trouve"

    model_id = (
        os.getenv("HF_MODEL_ID")
        or get_secret_value("HF_MODEL_ID")
        or "HuggingFaceH4/zephyr-7b-beta"
    )
    return token, model_id, source


def mask_token(token: Optional[str]) -> str:
    """Masque un token en gardant juste assez d'information pour diagnostiquer."""
    if not token:
        return "aucun"
    if len(token) <= 10:
        return f"{token[:3]}... ({len(token)} caracteres)"
    return f"{token[:3]}...{token[-4:]} ({len(token)} caracteres)"


HF_API_KEY, HF_MODEL_ID, HF_TOKEN_SOURCE = get_hf_config()

if not HF_API_KEY:
    st.error("HF_API_KEY non configuree. Ajoutez-la dans .env ou Streamlit secrets.")
    st.stop()

with st.sidebar.expander("Diagnostic Hugging Face"):
    st.caption(f"Source token : {HF_TOKEN_SOURCE}")
    st.caption(f"Token charge : {mask_token(HF_API_KEY)}")
    st.caption(f"Modele : {HF_MODEL_ID}")


def show_huggingface_permission_error() -> None:
    """Affiche une aide claire pour les erreurs de permissions HF."""
    st.error(
        "Votre token Hugging Face ne peut pas appeler Inference Providers. "
        "Creez un token fine-grained avec la permission "
        "'Make calls to Inference Providers', puis mettez a jour HF_API_KEY."
    )
    st.info(
        "Chemin Hugging Face : Settings > Access Tokens > Create new token > "
        "Fine-grained > cochez 'Make calls to Inference Providers'. "
        "Redemarrez Streamlit apres modification du fichier .env."
    )
    st.warning(
        f"Diagnostic actuel : Streamlit utilise {HF_TOKEN_SOURCE}, "
        f"token {mask_token(HF_API_KEY)}, modele {HF_MODEL_ID}."
    )

books_df, ratings_sample = load_rag_data()
if not validate_dataframe(books_df) or not validate_dataframe(ratings_sample):
    st.error("Impossible de charger les donnees. Executez d'abord python prepare_data.py.")
    st.stop()

try:
    books_ratings = ratings_sample.merge(books_df, on="book_id", how="inner")
    stats = books_ratings.groupby("book_id").agg(
        moyenne_note=("rating", "mean"),
        nb_votes=("rating", "count"),
        titre=("title", "first"),
        auteur=("authors", "first"),
        image=("small_image_url", "first"),
        goodreads=("goodreads_book_id", "first"),
        annee=("original_publication_year", "first"),
    ).reset_index()
    logger.info("Stats RAG calculees : %s livres", len(stats))
except Exception:
    logger.exception("Erreur lors du calcul des statistiques RAG")
    st.error("Erreur lors de la preparation des statistiques.")
    st.stop()

st.title("Assistant RAG pour les livres")

required_columns = ["title", "authors", "original_publication_year"]
missing_columns = [column for column in required_columns if column not in books_df.columns]
if missing_columns:
    st.error(f"Colonnes manquantes dans books.parquet : {', '.join(missing_columns)}")
    st.stop()

books_df = books_df.copy()
books_df["doc_text"] = books_df.apply(
    lambda row: (
        f"Titre: {row['title']} | Auteur: {row['authors']} | "
        f"Annee: {row['original_publication_year']}"
    ),
    axis=1,
)
documents = books_df["doc_text"].tolist()


@st.cache_resource(show_spinner="Initialisation du moteur de recherche...")
def init_faiss(docs: tuple[str, ...]):
    """Initialise le modele d'embeddings et l'index FAISS."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(list(docs), convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    logger.info("FAISS initialise avec %s documents", len(docs))
    return model, index


try:
    embed_model, index = init_faiss(tuple(documents))
except Exception:
    logger.exception("Erreur lors de l'initialisation FAISS")
    st.error("Erreur lors de l'initialisation du moteur de recherche.")
    st.stop()


def search_docs(query: str, k: int = 5) -> list[str]:
    """Retourne les documents les plus proches de la question."""
    try:
        q_emb = embed_model.encode([query], convert_to_numpy=True)
        _, indices = index.search(q_emb, k)
        return [documents[i] for i in indices[0] if 0 <= i < len(documents)]
    except Exception:
        logger.exception("Erreur lors de la recherche semantique")
        return []


user_question = st.text_area("Pose ta question :", height=100)

if st.button("Poser la question", key="rag_button"):
    if not user_question.strip():
        st.warning("Ecris ta question avant d'envoyer.")
        st.stop()

    try:
        with st.spinner("Recherche et generation en cours..."):
            client = InferenceClient(model=HF_MODEL_ID, token=HF_API_KEY)
            docs = search_docs(user_question, k=5)

            if not docs:
                st.warning("Aucun document pertinent trouve.")
                st.stop()

            context = "\n".join(docs)
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant qui repond aux questions sur des livres "
                        "en t'appuyant sur le contexte fourni."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Question : {user_question}\n\n"
                        f"Voici des extraits de livres :\n{context}\n\n"
                        "Reponds de maniere detaillee et structuree."
                    ),
                },
            ]
            response = client.chat_completion(
                model=HF_MODEL_ID,
                messages=messages,
                max_tokens=200,
            )

        st.success("Reponse generee")
        st.write("### Reponse enrichie :")
        st.write(response.choices[0].message["content"])

        with st.expander("Passages utilises"):
            for i, doc in enumerate(docs, 1):
                st.write(f"**{i}.** {doc}")

        logger.info("Question RAG traitee avec succes")
    except HfHubHTTPError as exc:
        logger.exception("Erreur Hugging Face")
        if getattr(exc.response, "status_code", None) == 403:
            show_huggingface_permission_error()
        else:
            st.error(f"Erreur Hugging Face : {exc}")
    except Exception as exc:
        logger.exception("Erreur lors du traitement RAG")
        st.error(f"Erreur lors du traitement : {exc}")

st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; font-size:14px; color:gray; margin-top:30px;'>
        Developpe par <a href="https://www.linkedin.com/in/daouda-ba-b9b21b2b4/" target="_blank" style="color:#0077b5;">Daouda Ba</a>
    </div>
    """,
    unsafe_allow_html=True,
)
