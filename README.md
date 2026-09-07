# Books_Project_Streamlit

Application Streamlit interactive pour analyser un catalogue de livres, explorer les donnees Goodreads et interroger un assistant RAG branche sur Hugging Face.

## Fonctionnalites

- Accueil du projet MauriBooks et presentation des phases API, data analysis et RAG.
- Dashboard Plotly avec metriques globales, auteurs, livres populaires, notes, annees de publication et langues.
- Explorateur de bibliotheque avec recherche rapide, filtres avances, couvertures et liens Goodreads.
- Assistant RAG avec embeddings Sentence Transformers, index FAISS et generation via Hugging Face Inference API.

## Architecture

```text
Books_Project_Streamlit/
├── streamlit_app/
│   ├── app.py
│   ├── accueil.py
│   ├── visualisation.py
│   ├── explorateur_bibliotheque.py
│   ├── rag.py
│   ├── prepare_data.py
│   ├── books.csv
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── logger.py
│   │   └── validators.py
│   └── .streamlit/
│       ├── config.toml
│       └── secrets.toml.example
├── output/
│   ├── books.parquet
│   ├── ratings.parquet
│   ├── tags.parquet
│   └── book_tags.parquet
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Creer un environnement virtuel

```bash
python -m venv env
```

Windows :

```bash
env\Scripts\activate
```

macOS/Linux :

```bash
source env/bin/activate
```

### 2. Installer les dependances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

Copiez `.env.example` vers `.env`, puis renseignez votre cle Hugging Face.

```env
HF_API_KEY=hf_your_key_here
HF_MODEL_ID=HuggingFaceH4/zephyr-7b-beta
BOOKS_API_URL=https://books-project-api.onrender.com
BATCH_SIZE=1000
LOG_LEVEL=INFO
```

Le fichier `.env` est ignore par Git. En production Streamlit, utilisez plutot `streamlit_app/.streamlit/secrets.toml`, base sur `secrets.toml.example`.

## Preparation des donnees

Depuis le dossier `streamlit_app` :

```bash
python prepare_data.py
```

Le script recupere les donnees via `mauribooks`, pagine les appels API, journalise les etapes et sauvegarde les fichiers parquet dans `output/`.

## Lancement

Depuis le dossier `streamlit_app` :

```bash
streamlit run app.py
```

L'application est disponible par defaut sur `http://localhost:8501`.

## Variables

| Variable | Description | Defaut |
| --- | --- | --- |
| `HF_API_KEY` | Cle API Hugging Face requise pour la page RAG. Le token doit autoriser les appels Inference Providers. | Aucun |
| `HF_MODEL_ID` | Modele LLM utilise par l'assistant | `HuggingFaceH4/zephyr-7b-beta` |
| `BOOKS_API_URL` | URL de l'API MauriBooks | `https://books-project-api.onrender.com` |
| `BATCH_SIZE` | Taille des pages lors de l'extraction API | `1000` |
| `LOG_LEVEL` | Niveau de logging Python | `INFO` |

## Qualite et securite

- Les secrets ne sont plus stockes dans le code source.
- Le chargement des donnees est centralise dans `streamlit_app/utils/data_loader.py`.
- Les validations DataFrame sont regroupees dans `streamlit_app/utils/validators.py`.
- Les logs passent par `streamlit_app/utils/logger.py`.
- Les fichiers locaux sensibles ou volumineux sont ignores dans `.gitignore`.

## Depannage

### `HF_API_KEY non configuree`

Verifiez que `.env` existe a la racine du projet et contient `HF_API_KEY`, puis redemarrez Streamlit.

### `403 Forbidden` Hugging Face Inference Providers

Le token utilise par l'application n'a pas la permission d'appeler Hugging Face Inference Providers.

Solution :

1. Ouvrez Hugging Face `Settings > Access Tokens`.
2. Creez un token `fine-grained`.
3. Cochez la permission `Make calls to Inference Providers`.
4. Remplacez `HF_API_KEY` dans `.env`.
5. Redemarrez Streamlit.

### `Impossible de charger les donnees`

Executez la preparation :

```bash
cd streamlit_app
python prepare_data.py
```

Verifiez ensuite que `output/books.parquet`, `output/ratings.parquet`, `output/tags.parquet` et `output/book_tags.parquet` existent.

### Port 8501 deja utilise

```bash
streamlit run app.py --server.port 8502
```

### Probleme FAISS sur Windows

Reinstallez la dependance :

```bash
pip install faiss-cpu
```

## Auteur

Daouda Ba

- LinkedIn : https://www.linkedin.com/in/daouda-ba-b9b21b2b4/
- GitHub : https://github.com/Daouda-Ba

## Licence

MIT License.
