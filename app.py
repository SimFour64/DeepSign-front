import streamlit as st

# Charger le CSS
def local_css(file_name):
    with open(file_name) as f:
        css_code = f.read()
    st.markdown(f'<style>{css_code}</style>', unsafe_allow_html=True)

# Appliquer le CSS
local_css("style.css")


# Definition des pages
Le_Projet = st.Page("pages/Le_Projet.py", title="Le Projet", icon="👋")
apprendre = st.Page("pages/Apprendre_les_signes.py", title="Apprendre les signes", icon="📋")
entrainer = st.Page("pages/S_entrainer.py", title="S'entrainer", icon="🎮")
quiz = st.Page("pages/quiz.py", title="Le Quiz des signes", icon="❓")

# Hierarchie des pages
pg = st.navigation(
    {
    "à propos":[Le_Projet],
    "commence à apprendre":[apprendre, entrainer,quiz]
    }
    )

# st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
