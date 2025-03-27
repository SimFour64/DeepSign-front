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


# Selecteur
col_1, col_2, col_3 = st.columns([0.1,0.8,0.1])

with col_2:
    options =  ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','Bye','Good','Good morning','Hello','Little bit','No','Pardon','Please','Project','Whats up','Yes']
    selection = st.pills("Choisis un mot :", options, selection_mode="single", default="1")
    if selection :
        col_selection = st.columns([0.2,0.3,0.3,0.2])
        col_selection[1].markdown(f"#### Essaie de reproduire le <strong style=' color:#75E6A4 ' >{selection}</strong>", unsafe_allow_html=True)
        img_path = f"media/signs/{selection.lower().replace(' ','')}.png"
        col_selection[2].image(img_path, width=80)


#####################################################################
# affichage des deux vignettes Vide/Response
#####################################################################

st.divider()

st.markdown("Place ta main dans le cadre vert 🎬")

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

with col_Video:
    image = capture_camera_input()

with col_Response:
    if st.button("Evaluer !"):
        response = requests.post(url_get_image_prediction_prod, files={"img": image} )
        if response.status_code == 200 :
            data = response.json()
            proba = round(max(data['probabilities'][0])*100,2)
            col_Retour_left, col_Retour_right = st.columns(2)
            bytes_data = image.getvalue()
            input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
            image = colored_img[Y1:Y2,X1:X2]
            col_Retour_left.image(image)
            if selection.lower() == data['prediction']:
                col_Retour_right.image("media/Man_saying_OK.png")
                st.success(f"✅ Bonne réponse : {data['prediction']}")
                st.success(f"Probabilité : {proba} %")
            else :
                col_Retour_right.image("media/Woman_saying_NO.png")

                st.error(f"❌ Mauvais signe : {data['prediction']}")
                st.error(f"Probabilité : {proba} %")
        else:
            st.error(f"Erreur API : {response.status_code}, {response.text}")
