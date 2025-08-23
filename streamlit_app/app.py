import streamlit as st

# Navigation
page_0 = st.Page("page0.py", title="Accueil")
page_1 = st.Page("page1.py", title="Aperçu")
page_2 = st.Page("page2.py", title="Insights sur les Tags")
page_3 = st.Page("page3.py", title="Explorateur de Livres")

pg = st.navigation([page_0, page_1, page_2, page_3])
pg.run()