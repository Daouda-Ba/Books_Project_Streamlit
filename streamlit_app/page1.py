import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- Configuration de la page ---
st.set_page_config(page_title="Analyse Mauribooks", layout="wide")

st.title("Analyse Générale des Livres et Évaluations (Mauribooks)")

# --- Charger les données Parquet ---
@st.cache_data
def load_data():
    output_dir = Path(__file__).resolve().parents[1] / "output"
    books_df = pd.read_parquet(output_dir / "books.parquet")
    ratings_df = pd.read_parquet(output_dir / "ratings.parquet")
    tags_df = pd.read_parquet(output_dir / "tags.parquet")
    book_tags_df = pd.read_parquet(output_dir / "book_tags.parquet")
    return books_df, ratings_df, tags_df, book_tags_df

books_df, ratings_df, tags_df, book_tags_df = load_data()

# --- Métriques globales ---
st.header("Vue d'ensemble")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Livres", f"{len(books_df):,}")
col2.metric("Total Évaluations", f"{len(ratings_df):,}")
col3.metric("Total Tags", f"{len(tags_df):,}")
col4.metric("Note Moyenne", f"{ratings_df['rating'].mean():.2f}/5")

st.divider()

# --- Top 10 Auteurs ---
st.subheader("Top 10 Auteurs par Nombre de Livres")
author_stats = books_df['authors'].value_counts().head(10).reset_index()
author_stats.columns = ["author_name", "book_count"]

fig_authors = px.bar(
    author_stats.sort_values("book_count"),
    x="book_count",
    y="author_name",
    orientation="h",
    color="book_count",
    color_continuous_scale="Greens",
    text="book_count"
)
fig_authors.update_traces(textposition='outside')
fig_authors.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
st.plotly_chart(fig_authors, use_container_width=True)

# --- Top 20 Livres par évaluations ---
st.subheader("Top 20 Livres par Nombre d'Évaluations")
top_books = ratings_df.groupby("book_id")['rating'].agg(['count','mean']).reset_index()
top_books.columns = ["book_id", "rating_count", "avg_rating"]
top_books = top_books.merge(books_df[['book_id','title']], on="book_id", how="left").sort_values("rating_count", ascending=False).head(20)
top_books["title_short"] = top_books["title"].apply(lambda x: x[:50]+"..." if len(str(x))>50 else str(x))

fig_top_books = px.bar(
    top_books.sort_values("rating_count"),
    x="rating_count",
    y="title_short",
    color="avg_rating",
    orientation="h",
    text="rating_count",
    labels={"title_short":"Titre du livre","rating_count":"Nombre d'évaluations","avg_rating":"Note moyenne"},
    color_continuous_scale="Viridis"
)
fig_top_books.update_traces(textposition='outside')
fig_top_books.update_layout(yaxis={'categoryorder':'total ascending'}, height=800)
st.plotly_chart(fig_top_books, use_container_width=True)

# --- Publications par année ---
if "original_publication_year" in books_df.columns:
    st.subheader("Livres Publiés par Année")
    books_filtered = books_df[(books_df["original_publication_year"].notna()) & (books_df["original_publication_year"]>1800)]
    books_by_year = books_filtered.groupby("original_publication_year")["book_id"].count().reset_index()
    books_by_year.columns = ["year", "book_count"]

    fig_by_year = px.line(
        books_by_year, x="year", y="book_count", markers=True,
        labels={"year":"Année","book_count":"Nombre de livres"}
    )
    fig_by_year.update_layout(height=500)
    st.plotly_chart(fig_by_year, use_container_width=True)