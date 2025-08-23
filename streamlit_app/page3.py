import streamlit as st
import pandas as pd
from pathlib import Path
import re

# ----- Configuration de la page -----
st.set_page_config(page_title="Explorateur Mauribooks", layout="wide")
st.title("Explorateur de livres")

# ----- Chargement des fichiers -----
output_dir = Path(__file__).resolve().parents[1] / "output"
books_df = pd.read_parquet(output_dir / "books.parquet")
ratings_df = pd.read_parquet(output_dir / "ratings.parquet")

# ----- Calcul des statistiques par livre -----
book_stats = ratings_df.groupby("book_id")["rating"].agg(["count", "mean"]).reset_index()
book_stats.columns = ["book_id", "rating_count", "avg_rating"]

# Ajouter le titre des livres
book_stats = book_stats.merge(
    books_df[["book_id", "title"]],
    on="book_id",
    how="left"
)

# ----- Filtres -----
with st.expander("Filtres avancés", expanded=True):
    col1, col2 = st.columns([1, 1])

    # Note moyenne min. (1 à 5)
    selected_rating = col1.slider("Note moyenne min.", 1, 5, 3)

    # Nombre de votes min.
    selected_votes = col2.slider(
        "Nombre d’évaluations min.",
        0, int(book_stats['rating_count'].max()), 10, 10
    )

    # Mot-clé dans le titre
    keyword = col2.text_input("Mot-clé dans le titre")

# ----- Bouton recherche -----
if st.button("Lancer la recherche"):

    filtered_books = book_stats.copy()

    # Filtrer par note et votes
    filtered_books = filtered_books[
        (filtered_books['avg_rating'] >= selected_rating) &
        (filtered_books['rating_count'] >= selected_votes)
    ]

    # Filtrer par mot-clé
    if keyword:
        filtered_books = filtered_books[
            filtered_books['title'].str.contains(keyword, case=False, na=False)
        ]

    # ----- Résumé -----
    st.markdown("## 🔎 Résultats de la recherche")
    k1, k2, k3 = st.columns(3)
    k1.metric("📚 Nombre de livres", len(filtered_books))
    k2.metric("⭐ Note moyenne", f"{filtered_books['avg_rating'].mean():.2f}" if not filtered_books.empty else "N/A")
    k3.metric("👥 Votes moyens", f"{filtered_books['rating_count'].mean():.0f}" if not filtered_books.empty else "N/A")

    # ----- Affichage des livres -----
    if filtered_books.empty:
        st.warning("Aucun livre ne correspond à vos critères.")
    else:
        for _, book in filtered_books.sort_values("avg_rating", ascending=False).iterrows():
            st.markdown(f"**{book['title']}** — ⭐ {book['avg_rating']:.1f} — {book['rating_count']} votes")
            st.divider()

else:
    st.info("Définissez vos filtres, puis cliquez sur **Lancer la recherche** pour explorer les livres.")