import streamlit as st

# ---------- CONFIG ----------
st.set_page_config(
    page_title="MauriBooks - Accueil",
    layout="wide",
)

# ---------- HEADER ----------
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("photo.jpg", width=100)

with col2:
    st.markdown(
        """
        <h1 style='text-align: center; color:#1f77b4; margin-bottom:0;'>
            MauriBooks
        </h1>
        <p style='text-align:center; font-size:18px; color:gray; margin-top:5px;'>
            Un projet en trois phases : <br>
            API • Data Analysis • RAG avec LLM
        </p>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style='text-align: right; font-size:18px;'>
            <a href="https://www.linkedin.com/in/daouda-ba-b9b21b2b4/" 
               target="_blank" 
               style='text-decoration: none; color: #0077b5;'>
                <strong>Daouda Ba</strong>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- PHASE 1 ----------
st.markdown("## Phase 1 : Développement API")

col1, col2 = st.columns([2, 3])
with col1:
    st.image("architecture.jpg", use_container_width=True, caption="Architecture de l’API")

with col2:
    st.markdown(
        """
        <div style="font-size:16px; line-height:1.6;">
        🔹 Conception et implémentation d’une API robuste pour gérer les données des livres. <br><br>
        🔹 Mise en place d’un pipeline d’ingestion des données. <br><br>
        🔹 Sauvegarde optimisée des données (<code>Parquet</code>).
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <a href="https://github.com/Daouda-Ba/Books_Project" target="_blank">
            <button style="background-color: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-size: 16px; cursor:pointer;">
                Voir le Code (Phase 1)
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- PHASE 2 ----------
st.markdown("## Phase 2 : Data Analysis & Visualisation")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div style="font-size:16px; line-height:1.6;">
        🔹 Développement d’une application Streamlit interactive. <br><br>
        🔹 Exploration des livres via des filtres avancés. <br><br>
        🔹 Création de visualisations dynamiques avec Plotly. <br><br>
        🔹 Expérience utilisateur moderne (multi-pages).
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <a href="https://github.com/Daouda-Ba/Books_Project_Streamlit" target="_blank">
            <button style="background-color: #0066cc; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-size: 16px; cursor:pointer;">
                Voir le Code (Phase 2)
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.image("architecture2.png", use_container_width=True, caption="Exploration et Visualisation")

st.markdown("---")

# ---------- PHASE 3 ----------
st.markdown("## Phase 3 : Assistant RAG avec LLM")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div style="font-size:16px; line-height:1.6;">
        🔹 Mise en place d’un RAG (Retrieval-Augmented Generation). <br><br>
        🔹 Indexation vectorielle des livres avec FAISS et Sentence Transformers. <br><br>
        🔹 Utilisation d’un LLM (Zephyr 7B) via Hugging Face. <br><br>
        🔹 Réponses enrichies basées sur le contenu des livres.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.image("rag.jpg", use_container_width=True, caption="Architecture RAG avec LLM")

st.markdown("---")

# ---------- FOOTER ----------
st.markdown(
    """
    <div style='text-align:center; font-size:14px; color:gray; margin-top:30px;'>
        <strong>MauriBooks</strong> Project — Developed by 
        <a href="https://www.linkedin.com/in/daouda-ba-b9b21b2b4/" 
           target="_blank" style="color:#0077b5;">Daouda Ba</a>
    </div>
    """,
    unsafe_allow_html=True,
)
