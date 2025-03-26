import os
import streamlit as st
import requests
import numpy as np
import cv2
from camera_input_live import camera_input_live
from streamlit.components.v1 import html

# Define the base URI of the API
#   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
#     on Streamlit Cloud
#   - The source selected is based on the shell variable passend when launching streamlit
#     (shortcuts are included in Makefile). By default it takes the cloud API url
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# Define the url to be used by requests.get to get a prediction (adapt if needed)
url = BASE_URI + 'predict'
url_get_image_prediction_prod = BASE_URI + "get_image_prediction_prod"

# Just displaying the source for the API. Remove this in your final version.
# st.markdown(f"Working with {url}")

# Define OpenCV box vertices
X1 = 150
X2 = 550
Y1 = 100
Y2 = 500


######################################################
#       Up Page
######################################################
st.title(" :grey[Entraine toi a reproduire un signe]")
# st.markdown("<p style='font-size:30px'align='right'>🎬</p>", unsafe_allow_html=True)
st.image("media/Training_4_signs.png", use_container_width=True)


# le Selecteur
col_1, col_2, col_3 = st.columns(3)

with col_2:
    options = ["C", "2", "Hello", "Please"]
    selection = st.pills("Choisis un mot :", options, selection_mode="single", default = "C")
    if selection :
        st.markdown(f"Essaie de reproduire le <strong style=' color:#75E6A4 ' >{selection}</strong>.", unsafe_allow_html=True)


######################################################
#        SELECT AND USE MODEL FROM GCP
######################################################


def get_available_models():
    response = requests.get(f"{BASE_URI}/models")  # Endpoint pour récupérer les modèles
    if response.status_code == 200:
        return response.json()['models']
    else:
        st.error(f"Erreur lors de la récupération des modèles : {response.status_code}")
        return []


# st.checkbox("Lancer la camera",key="checkbox_3")


image = camera_input_live(key="camera_input_3")

#####################################################################
# affichage des deux vignettes Vide/Response
#####################################################################
st.markdown("Place ta main dans le carré bleu 🎬")
col_Video, col_Response = st.columns(2)

with col_Video:
    # Custom HTML for video with specific dimensions and background
    # button =
    if image:
        # Image treatment to display back to the user with target rectangle
        bytes_data = image.getvalue()
        input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
        flipped_img = cv2.flip(colored_img, 1)
        annot_img = cv2.rectangle(flipped_img, (X1,Y1), (X2,Y2), (0,255,255), thickness=5, lineType=cv2.LINE_AA)
        st.image(annot_img)

    response = requests.post(url_get_image_prediction_prod, files={"img": image} )

with col_Response:
    if response.status_code == 200 :
        data = response.json()
        proba = round(max(data['probabilities'][0])*100,2)
        if selection.lower() == data['prediction']:
            st.image("media/Man_saying_OK.png")
            st.success(f"Signe prédit : {data['prediction']}")
            st.success(f"Probabilité : {proba} %")
        else :
            st.image("media/Woman_saying_NO.png")
            st.error(f"Signe prédit : {data['prediction']}")
            st.error(f"Probabilité : {proba} %")

    else:
        st.error(f"Erreur API : {response.status_code}, {response.text}")
