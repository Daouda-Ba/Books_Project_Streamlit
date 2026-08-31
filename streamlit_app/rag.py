import streamlit as st
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from huggingface_hub import InferenceClient

# --- Config page ---
st.set_page_config(page_title="Mauribooks", layout="wide")

# --- Chargement des données ---
@st.cache_data
def load_data():
    output_dir = Path(__file__).resolve().parents[1] / "output"
    books_df = pd.read_parquet(output_dir / "books.parquet")
    ratings_df = pd.read_parquet(output_dir / "ratings.parquet")
    books_csv = pd.read_csv("books.csv")

    # Fusionner pour récupérer toutes les colonnes utiles
    books_merged = books_df.merge(
        books_csv[["book_id", "goodreads_book_id", "image_url",
                   "small_image_url", "language_code", "original_publication_year"]],
        on="book_id", how="left"
    )

    # Échantillonner les ratings pour alléger
    ratings_sample = ratings_df.sample(n=500_000, random_state=42)
    return books_merged, ratings_sample

books_df, ratings_sample = load_data()

# Fusion livres + notes
books_ratings = ratings_sample.merge(books_df, on="book_id", how="inner")

# --- Statistiques globales ---
stats = books_ratings.groupby("book_id").agg(
    moyenne_note=("rating", "mean"),
    nb_votes=("rating", "count"),
    titre=("title", "first"),
    auteur=("authors", "first"),
    image=("small_image_url", "first"),
    goodreads=("goodreads_book_id", "first"),
    annee=("original_publication_year", "first")
).reset_index()

st.title("Assistant RAG pour les livres")


# Préparer les documents
books_df["doc_text"] = books_df.apply(
    lambda row: f"Titre: {row['title']} | Auteur: {row['authors']} | Année: {row['original_publication_year']}", axis=1
)
documents = books_df["doc_text"].tolist()

# Embeddings FAISS
@st.cache_resource
def init_faiss():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(documents, convert_to_numpy=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return model, index
embed_model, index = init_faiss()

# Recherche de docs
def search_docs(query, k=5):
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(q_emb, k)
    return [documents[i] for i in indices[0]]

# Initialiser le client Hugging Face
HF_API_KEY = "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" 
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"
client = InferenceClient(model=MODEL_ID, token=HF_API_KEY)

# Interface
user_question = st.text_area("Pose ta question :")

if st.button("Poser la question", key="rag_button"):
    if user_question.strip():
        with st.spinner("Recherche et génération en cours..."):
            # 1. Récupérer des passages pertinents
            docs = search_docs(user_question, k=5)
            context = "\n".join(docs)

            # 2. Construire les messages pour le modèle
            messages = [
                {"role": "system", "content": "Tu es un assistant qui répond aux questions sur des livres en t'appuyant sur le contexte fourni."},
                {"role": "user", "content": f"Question : {user_question}\n\nVoici des extraits de livres :\n{context}\n\nRéponds de manière détaillée et structurée."}
            ]

            # 3. Appeler le modèle
            response = client.chat_completion(
                model=MODEL_ID,
                messages=messages,
                max_tokens=200,
            )

            # 4. Afficher la réponse
            st.write("### Réponse enrichie :")
            st.write(response.choices[0].message["content"])

            # 5. Montrer les passages utilisés
            with st.expander("📖 Passages utilisés"):
                for d in docs:
                    st.write(d)
    else:
        st.warning("Écris ta question avant d’envoyer.")
        
st.markdown("---")

# ---------- FOOTER ----------
st.markdown(
    """
    <div style='text-align:center; font-size:14px; color:gray; margin-top:30px;'>
        Développé par <a href="https://www.linkedin.com/in/daouda-ba-b9b21b2b4/" target="_blank" style="color:#0077b5;">Daouda Ba</a>
    </div>
    """,
    unsafe_allow_html=True,
)