"""Page Explorateur - recherche et filtrage des livres."""

import pandas as pd
import streamlit as st

from utils.data_loader import load_explorer_data
from utils.logger import get_logger
from utils.validators import validate_dataframe

logger = get_logger(__name__)

st.set_page_config(page_title="Explorateur Mauribooks", layout="wide")

books_df, ratings_sample = load_explorer_data()
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
    logger.info("Explorateur pret : %s livres", len(stats))
except Exception:
    logger.exception("Erreur lors de la preparation de l'explorateur")
    st.error("Erreur lors de la preparation des donnees de recherche.")
    st.stop()

st.title("Explorateur de la Bibliotheque Mauribooks")
st.write(f"Nombre de livres disponibles : {len(books_df):,}")
st.write(f"Nombre d'evaluations echantillonnees : {len(ratings_sample):,}")

st.subheader("Recherche rapide")
search = st.text_input("Entrez un titre, auteur ou annee :")

if search:
    try:
        results = stats[
            stats["titre"].str.contains(search, case=False, na=False)
            | stats["auteur"].str.contains(search, case=False, na=False)
            | stats["annee"].astype(str).str.contains(search, case=False, na=False)
        ].sort_values("nb_votes", ascending=False).head(20)

        if results.empty:
            st.info("Aucun livre trouve.")
        else:
            st.dataframe(
                results[["titre", "auteur", "annee", "moyenne_note", "nb_votes"]],
                use_container_width=True,
            )

            cols = st.columns(5)
            for position, (_, row) in enumerate(results.iterrows()):
                with cols[position % 5]:
                    try:
                        if pd.notna(row["image"]) and pd.notna(row["goodreads"]):
                            st.markdown(
                                f'<a href="https://www.goodreads.com/book/show/{int(row["goodreads"])}" target="_blank">'
                                f'<img src="{row["image"]}" width="120"></a>',
                                unsafe_allow_html=True,
                            )
                        st.caption(f"{row['titre']} ({row['moyenne_note']:.2f}/5)")
                    except Exception:
                        logger.exception("Erreur affichage livre")
    except Exception:
        logger.exception("Erreur recherche rapide")
        st.error("Erreur lors de la recherche.")

st.subheader("Filtres avances")
with st.expander("Options de filtrage", expanded=True):
    col1, col2 = st.columns([1, 1])
    selected_rating = col1.slider("Note moyenne min.", 1, 5, 3)
    selected_votes = col2.slider(
        "Nombre d'evaluations min.",
        0,
        int(stats["nb_votes"].max()) if not stats.empty else 0,
        10,
        10,
    )
    keyword = col2.text_input("Mot-cle dans le titre")

if st.button("Lancer la recherche"):
    try:
        filtered_books = stats[
            (stats["moyenne_note"] >= selected_rating)
            & (stats["nb_votes"] >= selected_votes)
        ].copy()

        if keyword:
            filtered_books = filtered_books[
                filtered_books["titre"].str.contains(keyword, case=False, na=False)
            ]

        st.markdown("## Resultats de la recherche")
        k1, k2, k3 = st.columns(3)
        k1.metric("Nombre de livres", len(filtered_books))
        k2.metric(
            "Note moyenne",
            f"{filtered_books['moyenne_note'].mean():.2f}"
            if not filtered_books.empty
            else "N/A",
        )
        k3.metric(
            "Votes moyens",
            f"{filtered_books['nb_votes'].mean():.0f}"
            if not filtered_books.empty
            else "N/A",
        )

        if filtered_books.empty:
            st.warning("Aucun livre ne correspond a vos criteres.")
        else:
            cols = st.columns(5)
            sorted_books = filtered_books.sort_values("moyenne_note", ascending=False)
            for position, (_, book) in enumerate(sorted_books.iterrows()):
                with cols[position % 5]:
                    try:
                        if pd.notna(book["image"]) and pd.notna(book["goodreads"]):
                            st.markdown(
                                f'<a href="https://www.goodreads.com/book/show/{int(book["goodreads"])}" target="_blank">'
                                f'<img src="{book["image"]}" width="120"></a>',
                                unsafe_allow_html=True,
                            )
                        st.caption(
                            f"**{book['titre']}** - {book['moyenne_note']:.1f}/5 - "
                            f"{int(book['nb_votes'])} votes"
                        )
                    except Exception:
                        logger.exception("Erreur affichage livre filtre")
    except Exception:
        logger.exception("Erreur filtrage")
        st.error("Erreur lors du filtrage.")

st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; font-size:14px; color:gray; margin-top:30px;'>
        Developpe par <a href="https://www.linkedin.com/in/daouda-ba-b9b21b2b4/" target="_blank" style="color:#0077b5;">Daouda Ba</a>
    </div>
    """,
    unsafe_allow_html=True,
)
