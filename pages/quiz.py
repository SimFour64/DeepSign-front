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
quiz_words =  ['1','2','3','4','5','0','1','2','3']


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
- Utilise ta caméra pour montrer ton signe et clique sur Evaluer.
- Une coche verte ou une croix rouge apparaîtra selon ta réussite.
""")
######################
# Affichage progression
######################

st.markdown("### Progression du quiz :")
cols = st.columns(5)
for i, col in enumerate(cols):
    word = st.session_state.shuffled_words[i]
    if st.session_state.results[i] == "ok":
        col.image("media/valid.png", width=40)
        col.markdown(f"<div style='text-align: center; font-weight: bold;'>{word.capitalize()}</div>", unsafe_allow_html=True)
        col.image(f"media/signs/{word}.png", width=60)
    elif st.session_state.results[i] == "fail":
        col.image("media/wrong.png", width=40)
        col.markdown(f"<div style='text-align: center; font-weight: bold;'>{word.capitalize()}</div>", unsafe_allow_html=True)
        col.image(f"media/signs/{word}.png", width=60)
    else:
        col.image("media/question_mark.png", width=40)

# Afficher bouton de démarrage
if st.session_state.quiz_state == "waiting":
    if st.button("🚀 Commencer le quiz"):
        st.session_state.quiz_state = "in_progress"
        st.session_state.current_word_index = 0
        st.session_state.attempts = 0
        st.session_state.results = [None] * 5
        st.session_state.shuffled_words = random.sample(quiz_words, 5)
        st.rerun()

if st.session_state.quiz_state == "replay":
    st.session_state.quiz_state = "in_progress"
    st.session_state.current_word_index = 0
    st.session_state.attempts = 0
    st.session_state.results = [None] * 5
    st.session_state.shuffled_words = random.sample(quiz_words, 5)
    st.rerun()


# Partie active du quiz
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "awaiting_next" not in st.session_state:
    st.session_state.awaiting_next = False

elif st.session_state.quiz_state == "in_progress":

    current_word = st.session_state.shuffled_words[st.session_state.current_word_index]
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"### Mot à reproduire : :green[**{current_word.upper()}**]")
        st.write("Place ta main dans le cadre vert 🎬")


    col_Video, col_Response = st.columns(2)

    @st.fragment
    def capture_camera_input():
        image = camera_input_live()
        if image:
            bytes_data = image.getvalue()
            input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
            flipped_img = cv2.flip(colored_img, 1)
            annot_img = cv2.rectangle(flipped_img, (X1, Y1), (X2, Y2), (117, 230, 164), 5)
            st.image(annot_img)
        return image

    with col_Video:
        if "captured_image" not in st.session_state:
            st.session_state.captured_image = None

        image = capture_camera_input()
        if image:
            st.session_state.captured_image = image

    with col_Response:
        if not st.session_state.awaiting_next:
            if st.button("Evaluer !") and st.session_state.captured_image:
                response = requests.post(url_get_image_prediction_prod, files={"img": st.session_state.captured_image})
                if response.status_code == 200:
                    data = response.json()
                    proba = round(max(data['probabilities'][0]) * 100, 2)
                    prediction = data['prediction']

                    st.session_state.last_prediction = {
                        "prediction": prediction,
                        "proba": proba,
                        "image": st.session_state.captured_image
                    }

                    if prediction.lower() == current_word.lower():
                        st.session_state.results[st.session_state.current_word_index] = "ok"
                    else:
                        st.session_state.results[st.session_state.current_word_index] = "fail"

                    st.session_state.awaiting_next = True
                    st.rerun()
                else:
                    st.error(f"Erreur API : {response.status_code}, {response.text}")

        else:
            pred = st.session_state.last_prediction
            if st.button("➡️ Mot suivant"):
                st.session_state.current_word_index += 1
                st.session_state.attempts = 0
                st.session_state.last_prediction = None
                st.session_state.awaiting_next = False
                if st.session_state.current_word_index >= len(st.session_state.shuffled_words):
                    st.session_state.quiz_state = "done"

                st.rerun()
            if pred:
                col_Retour_left, col_Retour_right = st.columns(2)
                bytes_data = pred['image'].getvalue()
                input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                gray_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
                cropped_img = gray_img[Y1:Y2, X1:X2]
                col_Retour_left.image(cropped_img)

                # Résultat
                if pred['prediction'].lower() == current_word.lower():
                    col_Retour_right.image("media/Man_saying_OK.png")
                    st.success(f"✅ Bonne réponse : {pred['prediction']}")
                else:
                    col_Retour_right.image("media/Woman_saying_NO.png")
                    st.error(f"❌ Mauvais signe : {pred['prediction']}")
                st.markdown(f"**Probabilité : {pred['proba']}%**")


# Fin du quiz
elif st.session_state.quiz_state == "done":
    st.markdown("## 🎉 Fin du quiz !")
    score = st.session_state.results.count("ok")
    st.write(f"Ton score : **{score}/5**")
    if st.button("🔁 Rejouer"):
        st.session_state.quiz_state = "replay"
        st.rerun()
