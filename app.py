import os
import streamlit as st
import requests
import numpy as np
import cv2
from camera_input_live import camera_input_live

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
url_upload_image_preprod = BASE_URI + 'upload_image_preprod'
url_get_image_prediction = BASE_URI + 'get_image_prediction'

# Just displaying the source for the API. Remove this in your final version.
st.markdown(f"Working with {url}")

st.markdown("Now, the rest is up to you. Start creating your page.")


# TODO: Add some titles, introduction, ...
st.title("DeepSign — Démo de prédiction")

# TODO: Request user input
input_one = st.number_input("Valeur input_one", value=5.0)
input_two = st.number_input("Valeur input_two", value=10.0)

# TODO: Call the API using the user's input
#   - url is already defined above
#   - create a params dict based on the user's input
#   - finally call your API using the requests package
if st.button("Obtenir la prédiction"):
    params = {"input_one": input_one, "input_two": input_two}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json()["prediction"]
        st.success(f"✅ La prédiction est : **{prediction}**")
    else:
        st.error(f"Erreur API : {response.status_code}")

# TODO: retrieve the results
#   - add a little check if you got an ok response (status code 200) or something else
#   - retrieve the prediction from the JSON


# TODO: display the prediction in some fancy way to the user


# TODO: [OPTIONAL] maybe you can add some other pages?
#   - some statistical data you collected in graphs
#   - description of your product
#   - a 'Who are we?'-page

# UPLOAD IMAGE
st.title("DeepSign — Upload manuel d'image et récupération des informations")
st.markdown(f"Working with {url_get_image_prediction}")
uploaded_image = st.file_uploader("Choisissez une image à télécharger", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    st.image(uploaded_image, caption="Image téléchargée", use_container_width=True)

    if st.button("Envoyer l'image pour analyse"):
        response = requests.post(url_get_image_prediction, files={"img": uploaded_image})

        if response.status_code == 200:
            data = response.json()
            st.success(f"Signe prédit : {data['prediction']}")
            proba = round(max(data['probabilities'][0])*100,2)
            st.success(f"Probabilité : {proba} %")
        else:
            st.error(f"Erreur API : {response.status_code}")


# UPLOAD IMAGE FROM CAMERA + OPENCV
st.title("DeepSign — Upload via webcam et OpenCV et récupération des infos")
st.markdown(f"Working with {url_get_image_prediction}")

enable = st.checkbox("Launch video capturing")

if enable:
    c = st.columns(2)
    with c[0].container():
        image = camera_input_live()

        if image:
            # Image treatment to display back to the user with target rectangle
            bytes_data = image.getvalue()
            input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
            flipped_img = cv2.flip(colored_img, 1)
            annot_img = cv2.rectangle(flipped_img, (200,200), (500,500), (0,255,255), thickness=5, lineType=cv2.LINE_AA)
            st.image(annot_img)

    if c[1].button("Evaluate!"):
        # Once the user hits "Evaluate" button, the "pause" image is treated and sent to API
        cropped_img = cv2.flip(colored_img[200:500,200:500],1)
        height = 128
        width = 128
        std_dim = (height, width)
        resized_img = cv2.resize(cropped_img, std_dim)

        if image is not None:
            c[1].image(resized_img, caption="Image téléchargée", use_container_width=True)
            # !! The image sent to the API is the "raw" (not treated by OpenCV)
            response = requests.post(url_get_image_prediction, files={"img": image})

            if response.status_code == 200:
                data = response.json()
                c[1].success(f"Signe prédit : {data['prediction']}")
                proba = round(max(data['probabilities'][0])*100,2)
                c[1].success(f"Probabilité : {proba} %")
            else:
                c[1].error(f"Erreur API : {response.status_code}")
