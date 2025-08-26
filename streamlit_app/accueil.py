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
        <h1 style='text-align: center; color:#1f77b4;'>
            MauriBooks
        </h1>
        <p style='text-align:center; font-size:18px; color:gray;'>
            Un projet en deux phases : <br>
            Développement API & Analyse de données
        </p>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style='text-align: right; font-size:18px;'>
            <a href="https://www.linkedin.com/in/daouda-ba-b9b21b2b4/" target="_blank" style='text-decoration: none; color: #0077b5;'>
                <strong>Daouda Ba</strong>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- PHASE 1 ----------
st.markdown("## Phase 1 : Développeur Python & Architecte API")

col1, col2 = st.columns([2, 3])
with col1:
    st.image("photo.jpg", use_container_width=True, caption="Architecture API")

with col2:
    st.markdown(
        """
        <div style="font-size:16px; line-height:1.6;">
        🔹 Conception et implémentation d’une API robuste pour gérer les données des livres. <br><br>
        🔹 Mise en place d’un pipeline d’ingestion des données. <br><br>
        🔹 Sauvegarde des données (livres, évaluations, tags) dans un format optimisé <code>Parquet</code>.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <a href="https://github.com/Daouda-Ba/Books_Project" target="_blank">
            <button style="background-color: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-size: 16px; cursor:pointer;">
                Voir le Code de la Phase 1
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- PHASE 2 ----------
st.markdown("## Phase 2 : Data Analyst - Exploration et Visualisation")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div style="font-size:16px; line-height:1.6;">
        🔹 Développement d’une application **Streamlit** interactive. <br><br>
        🔹 Mise en place de filtres avancés pour explorer les livres. <br><br>
        🔹 Création de visualisations dynamiques avec **Plotly** et **Pandas**. <br><br>
        🔹 Expérience utilisateur moderne avec navigation multi-pages.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <a href="https://github.com/Daouda-Ba/Books_Project_Streamlit" target="_blank">
            <button style="background-color: #0066cc; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-size: 16px; cursor:pointer;">
                Voir le Code de la Phase 2
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.image("photo.jpg", use_container_width=True, caption="Exploration des données")

st.markdown("---")

# ---------- FOOTER ----------
st.markdown(
    """
    <div style='text-align:center; font-size:14px; color:gray; margin-top:30px;'>
        Développé par <a href="https://www.linkedin.com/in/daouda-ba-b9b21b2b4/" target="_blank" style="color:#0077b5;">Daouda Ba</a>
    </div>
    """,
    unsafe_allow_html=True,
)