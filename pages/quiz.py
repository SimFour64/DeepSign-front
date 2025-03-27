import os
import streamlit as st
import requests
import numpy as np
import cv2
from camera_input_live import camera_input_live
from streamlit.components.v1 import html
import random

# Define the base URI of the API
#   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
#     on Streamlit Cloud
#   - The source selected is based on the shell variable passend when launching streamlit
#     (shortcuts are included in Makefile). By default it takes the cloud API url

#TODO
# if 'API_URI' in os.environ:
#     BASE_URI = st.secrets[os.environ.get('API_URI')]
# else:
BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# Define the url to be used by requests.get to get a prediction (adapt if needed)
url = BASE_URI + 'predict'
url_get_image_prediction_prod = BASE_URI + "get_image_prediction_prod"

# Define OpenCV box vertices
X1 = 150
X2 = 550
Y1 = 100
Y2 = 500

# Liste des mots pour le quiz
#TODO
#quiz_words =  ['0','1','2','3','4','5','6','7','8','9','a','b','bye','c','d','e','good','good morning','hello','little bit','no','pardon','please','project','whats up','yes']
quiz_words =  ['2','2','2','2','2','2','2','2','2']


# Initialiser les états du jeu
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = "waiting"
    st.session_state.current_word_index = 0
    st.session_state.attempts = 0
    st.session_state.results = [None] * 5
    st.session_state.shuffled_words = random.sample(quiz_words, 5)

######################################################
#       Up Page
######################################################

st.title(":grey[Quiz interactif — Langage des signes américain]")
st.markdown("""
**Règles du jeu :**
- 5 mots à deviner.
- À chaque étape, un mot à reproduire s’affiche.
- Utilise ta caméra pour montrer ton signe et clique sur capturer.
- Tu as deux tentatives pour chaque mot.
- Une coche verte ou une croix rouge apparaîtra selon ta réussite.
""")


# Afficher bouton de démarrage
if st.session_state.quiz_state == "waiting":
    if st.button("🚀 Commencer le quiz"):
        st.session_state.quiz_state = "in_progress"
        st.session_state.current_word_index = 0
        st.session_state.attempts = 0
        st.session_state.results = [None] * 5
        st.session_state.shuffled_words = random.sample(quiz_words, 5)

        st.rerun()
# Afficher bouton de démarrage
if st.session_state.quiz_state == "replay":
    st.session_state.quiz_state = "in_progress"
    st.session_state.current_word_index = 0
    st.session_state.attempts = 0
    st.session_state.results = [None] * 5
    st.session_state.shuffled_words = random.sample(quiz_words, 5)

    st.rerun()

# Partie active du quiz
elif st.session_state.quiz_state == "in_progress":

    ######################
    # Affichage progression
    ######################

    st.markdown("### Progression du quiz :")
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if st.session_state.results[i] == "ok":
            col.image("media/valid.png", width=40)
            col.markdown(f"**{st.session_state.shuffled_words[i].capitalize()}**")
        elif st.session_state.results[i] == "fail":
            col.image("media/wrong.png", width=40)
            col.markdown(f"**{st.session_state.shuffled_words[i].capitalize()}**")
        else:
            col.image("media/question_mark.png", width=40)

    ######################
    # Mot à deviner
    ######################

    current_word = st.session_state.shuffled_words[st.session_state.current_word_index]
    st.markdown(f"### Mot à reproduire : :green[**{current_word.upper()}**]")
    st.write("Place ta main dans le cadre vert 🎬")

    ######################
    # Capture & prédiction
    ######################

    col_Video, col_Response = st.columns(2)
    @st.fragment
    def capture_camera_input():
        image = camera_input_live()
        if image:
            # Image treatment to display back to the user with target rectangle
            bytes_data = image.getvalue()
            input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
            flipped_img = cv2.flip(colored_img, 1)
            annot_img = cv2.rectangle(flipped_img, (X1,Y1), (X2,Y2), (117,230,164), thickness=5, lineType=cv2.LINE_AA)
            st.image(annot_img)
        return image

    @st.fragment
    def display_true():
        col_Retour_right.image("media/Man_saying_OK.png")
        st.success(f"✅ Bonne réponse : {prediction}")
        st.success(f"Probabilité : {proba} %")
        st.session_state.results[st.session_state.current_word_index] = "ok"
        st.session_state.current_word_index += 1
        st.session_state.attempts = 0

    @st.fragment
    def display_false():
        col_Retour_right.image("media/Woman_saying_NO.png")
        st.error(f"❌ Mauvais signe : {prediction}")
        st.error(f"Probabilité : {proba} %")
        st.session_state.attempts += 1
        if st.session_state.attempts >= 2:
            st.session_state.results[st.session_state.current_word_index] = "fail"
            st.session_state.current_word_index += 1
            st.session_state.attempts = 0

    with col_Video:
        image = capture_camera_input()

    with col_Response:
        if st.session_state.attempts >= 2 or st.session_state.results[st.session_state.current_word_index] == "ok":
            if st.button("Suivant ->"):
                st.rerun()

        elif st.button("Evaluer !"):
            response = requests.post(url_get_image_prediction_prod, files={"img": image})
            if response.status_code == 200:
                data = response.json()
                proba = round(max(data['probabilities'][0]) * 100, 2)
                col_Retour_left, col_Retour_right = st.columns(2)
                bytes_data = image.getvalue()
                input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
                image = colored_img[Y1:Y2,X1:X2]
                col_Retour_left.image(image)
                prediction = data['prediction']
                if prediction.lower() == current_word.lower():
                    display_true()
                else:
                    display_false()

                # Fin de quiz
                if st.session_state.current_word_index >= len(st.session_state.shuffled_words):
                    st.session_state.quiz_state = "done"
                #st.rerun()
            else:
                st.error(f"Erreur API : {response.status_code}, {response.text}")

# Fin du quiz
elif st.session_state.quiz_state == "done":
    st.markdown("## 🎉 Fin du quiz !")
    score = st.session_state.results.count("ok")
    st.write(f"Ton score : **{score}/5**")
    if st.button("🔁 Rejouer"):
        st.session_state.quiz_state = "replay"
        st.rerun()
