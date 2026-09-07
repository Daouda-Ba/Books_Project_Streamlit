"""Script de preparation des donnees avec pagination et logging."""

import os
from pathlib import Path
from typing import Callable

import pandas as pd
from dotenv import load_dotenv
from mauribooks import BookClient, BookConfig

from utils.logger import get_logger

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)

logger = get_logger(__name__)
API_BASE_URL = os.getenv("BOOKS_API_URL", "https://books-project-api.onrender.com")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def fetch_paginated_data(
    client_method: Callable[..., pd.DataFrame],
    item_name: str,
    batch_size: int = BATCH_SIZE,
) -> pd.DataFrame:
    """Recupere toutes les pages d'un endpoint MauriBooks."""
    all_data: list[pd.DataFrame] = []
    skip = 0

    try:
        while True:
            batch = client_method(skip=skip, limit=batch_size, output_format="pandas")
            if batch.empty:
                break

            all_data.append(batch)
            skip += batch_size
            logger.info("Recupere %s %s...", skip, item_name)

        result = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
        logger.info("Total %s : %s lignes", item_name, len(result))
        return result
    except Exception:
        logger.exception("Erreur lors de la recuperation de %s", item_name)
        return pd.DataFrame()


def save_parquet(df: pd.DataFrame, filename: str) -> None:
    """Sauvegarde un DataFrame non vide au format parquet."""
    if df.empty:
        logger.warning("%s non sauvegarde : aucune donnee recue", filename)
        return

    path = OUTPUT_DIR / filename
    df.to_parquet(path, index=False)
    logger.info("%s sauvegarde (%s lignes)", filename, len(df))


def main() -> None:
    """Recupere et sauvegarde les datasets utilises par l'application."""
    logger.info("Connexion a l'API : %s", API_BASE_URL)
    config = BookConfig(book_base_url=API_BASE_URL)
    client = BookClient(config=config)

    datasets = {
        "books.parquet": (client.list_books, "livres"),
        "ratings.parquet": (client.list_ratings, "evaluations"),
        "tags.parquet": (client.list_tags, "tags"),
        "book_tags.parquet": (client.list_book_tags, "book_tags"),
    }

    for filename, (client_method, item_name) in datasets.items():
        logger.info("Recuperation des %s...", item_name)
        data = fetch_paginated_data(client_method, item_name)
        save_parquet(data, filename)

    logger.info("Preparation des donnees terminee")


if __name__ == "__main__":
    main()
