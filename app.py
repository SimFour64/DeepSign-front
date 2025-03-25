import streamlit as st

Le_Projet = st.Page("pages/Le_Projet.py", title="Le Projet", icon="👋")
apprendre = st.Page("pages/Apprendre_les_signes.py", title="Apprendre les signes", icon="📋")
entrainer = st.Page("pages/S_entrainer.py", title="S'entrainer", icon="🎮")

pg = st.navigation(
    {
    "à propos":[Le_Projet],
    "commence à apprendre":[apprendre, entrainer]
    }
    )


st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
