import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Explorateur Mauribooks", layout="wide")

@st.cache_data
def load_data():
    output_dir = Path(__file__).resolve().parents[1] / "output"

    # Charger les datasets
    books_df = pd.read_parquet(output_dir / "books.parquet")
    ratings_df = pd.read_parquet(output_dir / "ratings.parquet")
    books_csv = pd.read_csv("books.csv")

    # Fusionner pour récupérer toutes les colonnes utiles
    books_merged = books_df.merge(
        books_csv[
            ["book_id", "goodreads_book_id", "image_url",
             "small_image_url", "language_code", "original_publication_year"]
        ],
        on="book_id",
        how="left"
    )

    # Échantillonner les ratings pour alléger
    ratings_sample = ratings_df.sample(n=500_000, random_state=42)

    return books_merged, ratings_sample

# === Chargement des données ===
books_df, ratings_sample = load_data()

# Fusion livres + notes
books_ratings = ratings_sample.merge(books_df, on="book_id", how="inner")

# === Interface ===
st.title("Explorateur de la Bibliothèque Mauribooks")
st.write(f"Nombre de livres disponibles : {len(books_df):,}")
st.write(f"Nombre d'évaluations échantillonnées : {len(ratings_sample):,}")

# Statistiques globales par livre
stats = books_ratings.groupby("book_id").agg(
    moyenne_note=("rating", "mean"),
    nb_votes=("rating", "count"),
    titre=("title", "first"),
    auteur=("authors", "first"),
    image=("small_image_url", "first"),
    goodreads=("goodreads_book_id", "first"),
    annee=("original_publication_year", "first")
).reset_index()


# === Recherche simple ===
st.subheader("Recherche rapide")
search = st.text_input("Entrez un titre, auteur ou année :")

if search:
    results = stats[
        stats["titre"].str.contains(search, case=False, na=False) |
        stats["auteur"].str.contains(search, case=False, na=False) |
        stats["annee"].astype(str).str.contains(search, case=False, na=False)
    ].sort_values("nb_votes", ascending=False).head(20)

    if not results.empty:
        st.dataframe(results[["titre", "auteur", "annee", "moyenne_note", "nb_votes"]])

        # Affichage des couvertures cliquables
        cols = st.columns(5)
        for i, row in results.iterrows():
            with cols[i % 5]:
                if pd.notna(row["image"]):
                    st.markdown(
                        f'<a href="https://www.goodreads.com/book/show/{int(row["goodreads"])}" target="_blank">'
                        f'<img src="{row["image"]}" width="120"></a>',
                        unsafe_allow_html=True
                    )
                st.caption(f"{row['titre']} ({row['moyenne_note']:.2f}⭐)")
    else:
        st.info("Aucun livre trouvé.")


# === Filtres avancés ===
st.subheader("Filtres avancés")
with st.expander("Options de filtrage", expanded=True):
    col1, col2 = st.columns([1, 1])

    # Note moyenne min. (1 à 5)
    selected_rating = col1.slider("Note moyenne min.", 1, 5, 3)

    # Nombre de votes min.
    selected_votes = col2.slider(
        "Nombre d’évaluations min.",
        0, int(stats['nb_votes'].max()), 10, 10
    )

    # Mot-clé dans le titre
    keyword = col2.text_input("Mot-clé dans le titre")

# ----- Bouton recherche -----
if st.button("Lancer la recherche"):
    filtered_books = stats.copy()

    # Filtrer par note et votes
    filtered_books = filtered_books[
        (filtered_books['moyenne_note'] >= selected_rating) &
        (filtered_books['nb_votes'] >= selected_votes)
    ]

    # Filtrer par mot-clé
    if keyword:
        filtered_books = filtered_books[
            filtered_books['titre'].str.contains(keyword, case=False, na=False)
        ]

    # ----- Résumé -----
    st.markdown("## 🔎 Résultats de la recherche")
    k1, k2, k3 = st.columns(3)
    k1.metric("📚 Nombre de livres", len(filtered_books))
    k2.metric("⭐ Note moyenne", f"{filtered_books['moyenne_note'].mean():.2f}" if not filtered_books.empty else "N/A")
    k3.metric("👥 Votes moyens", f"{filtered_books['nb_votes'].mean():.0f}" if not filtered_books.empty else "N/A")

    # ----- Affichage des livres -----
    if filtered_books.empty:
        st.warning("Aucun livre ne correspond à vos critères.")
    else:
        cols = st.columns(5)
        for i, book in filtered_books.sort_values("moyenne_note", ascending=False).iterrows():
            with cols[i % 5]:
                if pd.notna(book["image"]):
                    st.markdown(
                        f'<a href="https://www.goodreads.com/book/show/{int(book["goodreads"])}" target="_blank">'
                        f'<img src="{book["image"]}" width="120"></a>',
                        unsafe_allow_html=True
                    )
                st.caption(f"**{book['titre']}** — ⭐ {book['moyenne_note']:.1f} — {book['nb_votes']} votes")