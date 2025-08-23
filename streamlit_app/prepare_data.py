import pandas as pd
from pathlib import Path
from mauribooks import BookClient, BookConfig

output_dir = Path(__file__).resolve().parents[1] / "output"
output_dir.mkdir(exist_ok=True)

# --- Init SDK ---
config = BookConfig(book_base_url="https://books-project-api.onrender.com")
client = BookClient(config=config)

# --- Fonction pour récupérer toutes les données avec pagination ---
def fetch_all_books(batch_size=1000):
    all_books = []
    skip = 0
    while True:
        batch = client.list_books(skip=skip, limit=batch_size, output_format="pandas")
        if batch.empty:
            break
        all_books.append(batch)
        skip += batch_size
        print(f"Récupéré {skip} livres...")
    return pd.concat(all_books, ignore_index=True) if all_books else pd.DataFrame()

def fetch_all_ratings(batch_size=1000):
    all_ratings = []
    skip = 0
    while True:
        batch = client.list_ratings(skip=skip, limit=batch_size, output_format="pandas")
        if batch.empty:
            break
        all_ratings.append(batch)
        skip += batch_size
        print(f"Récupéré {skip} évaluations...")
    return pd.concat(all_ratings, ignore_index=True) if all_ratings else pd.DataFrame()

def fetch_all_tags(batch_size=1000):
    all_tags = []
    skip = 0
    while True:
        batch = client.list_tags(skip=skip, limit=batch_size, output_format="pandas")
        if batch.empty:
            break
        all_tags.append(batch)
        skip += batch_size
        print(f"Récupéré {skip} tags...")
    return pd.concat(all_tags, ignore_index=True) if all_tags else pd.DataFrame()

def fetch_all_book_tags(batch_size=1000):
    all_book_tags = []
    skip = 0
    while True:
        batch = client.list_book_tags(skip=skip, limit=batch_size, output_format="pandas")
        if batch.empty:
            break
        all_book_tags.append(batch)
        skip += batch_size
        print(f"Récupéré {skip} book_tags...")
    return pd.concat(all_book_tags, ignore_index=True) if all_book_tags else pd.DataFrame()


# --- Récupération des données ---
print("Récupération des livres...")
books_df = fetch_all_books()
books_df.to_parquet(output_dir / "books.parquet", index=False)

print("Récupération des évaluations...")
ratings_df = fetch_all_ratings()
ratings_df.to_parquet(output_dir / "ratings.parquet", index=False)

print("Récupération des tags...")
tags_df = fetch_all_tags()
tags_df.to_parquet(output_dir / "tags.parquet", index=False)

print("Récupération des book_tags...")
book_tags_df = fetch_all_book_tags()
book_tags_df.to_parquet(output_dir / "book_tags.parquet", index=False)

print("Toutes les données ont été sauvegardées dans 'output/'")