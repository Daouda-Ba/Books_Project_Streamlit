import streamlit as st

# Navigation
page_0 = st.Page("accueil.py", title="Accueil")
page_1 = st.Page("visualisation.py", title="Visualisation")
page_2 = st.Page("explorateur_bibliotheque.py", title="Explorateur Bibliothèque")
page_3 = st.Page("rag.py", title="AI Assistant")

pg = st.navigation([page_0, page_1, page_2, page_3])
pg.run()