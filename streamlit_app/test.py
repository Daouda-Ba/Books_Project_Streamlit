from huggingface_hub import InferenceClient

# Initialise le client avec ton token
client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",  # modèle TGI hébergé
    token="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"  # ton token HF
)

# Exemple d'appel pour du chat
response = client.chat_completion(
    model="HuggingFaceH4/zephyr-7b-beta",
    messages=[
        {"role": "system", "content": "Tu es un assistant utile."},
        {"role": "user", "content": "Explique-moi la différence entre RAG et fine-tuning."}
    ],
    max_tokens=200,
)

print(response.choices[0].message["content"])




# User : Il saisit une requête, pose une question, ou entre des données dans l’interface Streamlit.

# Streamlit : Reçoit l’action de l’utilisateur, Transmet la requête sous forme de requête HTTP vers  l'API.

# API (Back-End / Traitement) : Reçoit la requête envoyée par Streamlit, Exécute la logique métier (ex. : appeler ton modèle IA, interroger une base de données, faire des calculs) et Retourne une réponse JSON avec les résultats.

# Retour de l’API vers Streamlit

# Streamlit récupère la réponse JSON.

# Les résultats sont affichés dans l’interface utilisateur



# API Users (clients de l’API) : Ce sont les utilisateurs ou applications qui consomment notre API.

# SDK : Un kit de développement logiciel (Software Development Kit) qui facilite l’interaction entre l’utilisateur et l’API.

# Data Transfer and Validation (Pydantic) : Pydantic est utilisé pour valider et sérialiser les données échangées. Avant qu’une requête ne soit traitée, les données sont vérifiées (format, type, contraintes).

# API Controller (FastAPI) : C’est le cœur de l’API, construit avec FastAPI. Il reçoit les requêtes, applique la logique métier, et appelle la base de données si nécessaire.

# Database Classes (SQLAlchemy) : C’est la couche d’accès aux données. SQLAlchemy gère la communication entre l’API et la base de données. Les modèles de données y sont définis (tables, relations...etc).

# Database (SQLite) : La base de données utilisée ici est SQLite. Elle stocke toutes les informations nécessaires à l’application