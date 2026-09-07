"""Chargement centralise des donnees de l'application."""

from pathlib import Path
from typing import Tuple

import pandas as pd
import streamlit as st

from .logger import get_logger

logger = get_logger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "streamlit_app"
OUTPUT_DIR = PROJECT_ROOT / "output"
BOOKS_CSV = APP_DIR / "books.csv"
RATINGS_SAMPLE_SIZE = 500_000


def _read_parquet(name: str) -> pd.DataFrame:
    path = OUTPUT_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    return pd.read_parquet(path)


def _read_books_csv() -> pd.DataFrame:
    if not BOOKS_CSV.exists():
        raise FileNotFoundError(f"Fichier introuvable : {BOOKS_CSV}")
    return pd.read_csv(BOOKS_CSV)


def _sample_ratings(ratings_df: pd.DataFrame) -> pd.DataFrame:
    if len(ratings_df) <= RATINGS_SAMPLE_SIZE:
        return ratings_df.copy()
    return ratings_df.sample(n=RATINGS_SAMPLE_SIZE, random_state=42)


def _merge_books_metadata(books_df: pd.DataFrame, books_csv: pd.DataFrame) -> pd.DataFrame:
    metadata_columns = {
        "goodreads_book_id",
        "image_url",
        "small_image_url",
        "language_code",
        "original_publication_year",
    }
    columns_to_add = [
        column
        for column in metadata_columns
        if column in books_csv.columns and column not in books_df.columns
    ]
    available_columns = ["book_id", *columns_to_add] if "book_id" in books_csv.columns else []

    if "book_id" not in available_columns:
        logger.warning("books.csv ne contient pas book_id, fusion metadata ignoree")
        return books_df.copy()

    if len(available_columns) == 1:
        return books_df.copy()

    return books_df.merge(books_csv[available_columns], on="book_id", how="left")


@st.cache_data(show_spinner="Chargement des donnees RAG...")
def load_rag_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Charge les livres et un echantillon de notes pour la page RAG."""
    try:
        books_df = _read_parquet("books.parquet")
        ratings_df = _read_parquet("ratings.parquet")
        books_csv = _read_books_csv()
        books_merged = _merge_books_metadata(books_df, books_csv)
        ratings_sample = _sample_ratings(ratings_df)
        logger.info(
            "Donnees RAG chargees : %s livres, %s evaluations",
            len(books_merged),
            len(ratings_sample),
        )
        return books_merged, ratings_sample
    except Exception:
        logger.exception("Erreur lors du chargement des donnees RAG")
        return pd.DataFrame(), pd.DataFrame()


@st.cache_data(show_spinner="Chargement des donnees de visualisation...")
def load_viz_data() -> Tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
]:
    """Charge les donnees necessaires au dashboard de visualisation."""
    try:
        books_df = _read_parquet("books.parquet")
        ratings_df = _read_parquet("ratings.parquet")
        tags_df = _read_parquet("tags.parquet")
        book_tags_df = _read_parquet("book_tags.parquet")
        books_csv = _read_books_csv()
        logger.info("Donnees de visualisation chargees")
        return books_df, ratings_df, tags_df, book_tags_df, books_csv
    except Exception:
        logger.exception("Erreur lors du chargement des donnees de visualisation")
        return (
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame(),
        )


@st.cache_data(show_spinner="Chargement de l'explorateur...")
def load_explorer_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Charge les livres et un echantillon de notes pour l'explorateur."""
    try:
        books_df = _read_parquet("books.parquet")
        ratings_df = _read_parquet("ratings.parquet")
        books_csv = _read_books_csv()
        books_merged = _merge_books_metadata(books_df, books_csv)
        ratings_sample = _sample_ratings(ratings_df)
        logger.info(
            "Donnees explorateur chargees : %s livres, %s evaluations",
            len(books_merged),
            len(ratings_sample),
        )
        return books_merged, ratings_sample
    except Exception:
        logger.exception("Erreur lors du chargement des donnees explorateur")
        return pd.DataFrame(), pd.DataFrame()
