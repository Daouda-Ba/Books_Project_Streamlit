"""Page Visualisation - dashboard d'analyse des livres."""

import plotly.express as px
import streamlit as st

from utils.data_loader import load_viz_data
from utils.logger import get_logger
from utils.validators import truncate_title, validate_dataframe

logger = get_logger(__name__)

st.set_page_config(page_title="Analyse Mauribooks", layout="wide")
st.title("Analyse Generale des Livres et Evaluations")

books_df, ratings_df, tags_df, book_tags_df, books_csv = load_viz_data()
if not validate_dataframe(books_df) or not validate_dataframe(ratings_df):
    st.error("Impossible de charger les donnees. Executez d'abord python prepare_data.py.")
    st.stop()

st.header("Vue d'ensemble")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Livres", f"{len(books_df):,}")
col2.metric("Total Evaluations", f"{len(ratings_df):,}")
col3.metric("Total Tags", f"{len(tags_df):,}" if validate_dataframe(tags_df) else "N/A")
col4.metric("Note Moyenne", f"{ratings_df['rating'].mean():.2f}/5")

st.divider()

try:
    st.subheader("Top 10 Auteurs par Nombre de Livres")
    author_stats = books_df["authors"].value_counts().head(10).reset_index()
    author_stats.columns = ["author_name", "book_count"]

    fig_authors = px.bar(
        author_stats.sort_values("book_count"),
        x="book_count",
        y="author_name",
        orientation="h",
        color="book_count",
        color_continuous_scale="Greens",
        text="book_count",
    )
    fig_authors.update_traces(textposition="outside")
    fig_authors.update_layout(yaxis={"categoryorder": "total ascending"}, height=400)
    st.plotly_chart(fig_authors, use_container_width=True)
except Exception:
    logger.exception("Erreur top auteurs")
    st.warning("Le graphique des auteurs n'a pas pu etre affiche.")

try:
    st.subheader("Top 20 Livres par Nombre d'Evaluations")
    top_books = ratings_df.groupby("book_id")["rating"].agg(["count", "mean"]).reset_index()
    top_books.columns = ["book_id", "rating_count", "avg_rating"]
    top_books = (
        top_books.merge(books_df[["book_id", "title"]], on="book_id", how="left")
        .sort_values("rating_count", ascending=False)
        .head(20)
    )
    top_books["title_short"] = top_books["title"].apply(truncate_title)

    fig_top_books = px.bar(
        top_books.sort_values("rating_count"),
        x="rating_count",
        y="title_short",
        color="avg_rating",
        orientation="h",
        text="rating_count",
        labels={
            "title_short": "Titre du livre",
            "rating_count": "Nombre d'evaluations",
            "avg_rating": "Note moyenne",
        },
        color_continuous_scale="Viridis",
    )
    fig_top_books.update_traces(textposition="outside")
    fig_top_books.update_layout(yaxis={"categoryorder": "total ascending"}, height=800)
    st.plotly_chart(fig_top_books, use_container_width=True)
except Exception:
    logger.exception("Erreur top livres")
    st.warning("Le graphique des livres les plus evalues n'a pas pu etre affiche.")

try:
    if "original_publication_year" in books_df.columns:
        st.subheader("Livres Publies par Annee")
        books_filtered = books_df[
            books_df["original_publication_year"].notna()
            & (books_df["original_publication_year"] > 1800)
        ]
        books_by_year = (
            books_filtered.groupby("original_publication_year")["book_id"]
            .count()
            .reset_index()
        )
        books_by_year.columns = ["year", "book_count"]

        fig_by_year = px.line(
            books_by_year,
            x="year",
            y="book_count",
            markers=True,
            labels={"year": "Annee", "book_count": "Nombre de livres"},
        )
        fig_by_year.update_layout(height=500)
        st.plotly_chart(fig_by_year, use_container_width=True)
except Exception:
    logger.exception("Erreur publications par annee")

try:
    if "average_rating" in books_df.columns:
        st.subheader("Distribution des Notes Moyennes")
        fig_ratings = px.histogram(
            books_df,
            x="average_rating",
            nbins=30,
            color_discrete_sequence=["#636EFA"],
        )
        fig_ratings.update_layout(
            xaxis_title="Note Moyenne",
            yaxis_title="Nombre de Livres",
            height=500,
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
except Exception:
    logger.exception("Erreur distribution des notes")

try:
    st.subheader("Popularite vs Qualite")
    popularity_df = ratings_df.groupby("book_id")["rating"].agg(["count", "mean"]).reset_index()
    popularity_df.columns = ["book_id", "rating_count", "avg_rating"]
    popularity_df = popularity_df.merge(
        books_df[["book_id", "title"]], on="book_id", how="left"
    )

    fig_popularity = px.scatter(
        popularity_df,
        x="rating_count",
        y="avg_rating",
        hover_data=["title"],
        size="rating_count",
        size_max=40,
        color="avg_rating",
        color_continuous_scale="Turbo",
        labels={"rating_count": "Nombre d'evaluations", "avg_rating": "Note Moyenne"},
    )
    fig_popularity.update_layout(height=600, xaxis_type="log")
    st.plotly_chart(fig_popularity, use_container_width=True)
except Exception:
    logger.exception("Erreur popularite vs qualite")

try:
    if "language_code" in books_csv.columns:
        st.subheader("Top 10 Langues les Plus Representees")
        lang_stats = books_csv["language_code"].value_counts().head(10).reset_index()
        lang_stats.columns = ["language", "book_count"]

        fig_lang = px.bar(
            lang_stats,
            x="book_count",
            y="language",
            orientation="h",
            text="book_count",
            color="book_count",
            color_continuous_scale="Plasma",
        )
        fig_lang.update_traces(textposition="outside")
        fig_lang.update_layout(height=500, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_lang, use_container_width=True)
except Exception:
    logger.exception("Erreur langues")

st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; font-size:14px; color:gray; margin-top:30px;'>
        Developpe par <a href="https://www.linkedin.com/in/daouda-ba-b9b21b2b4/" target="_blank" style="color:#0077b5;">Daouda Ba</a>
    </div>
    """,
    unsafe_allow_html=True,
)
