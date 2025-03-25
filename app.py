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
url_get_image_prediction_from_gcp_model_5 = BASE_URI + 'get_image_prediction_from_gcp_model_5'
url_get_image_prediction_from_gcp_model_full = BASE_URI + 'get_image_prediction_from_gcp_model_full'
url_get_image_prediction = BASE_URI + 'get_image_prediction'

# Just displaying the source for the API. Remove this in your final version.
st.markdown(f"Working with {url}")

# Define OpenCV box vertices
X1 = 100
X2 = 600
Y1 = 25
Y2 = 525


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

##### 5 CLASSES  #####
st.title("DeepSign — Upload via webcam et OpenCV et predict avec le model GCP 5 CLASSES")
st.markdown(f"Working with {url_get_image_prediction_from_gcp_model_5}")

all_gcp_models = get_available_models()

filtered_models_5 = [m for m in all_gcp_models if "5classes/" in m and m.endswith(".keras")]

if filtered_models_5:
    models_dict = {m.split('/')[-1]: m for m in filtered_models_5}
    selected_model_name  = st.selectbox("Sélectionnez un modèle", list(models_dict.keys()),key="selectbox_2")
    selected_model = models_dict[selected_model_name]

     # Afficher l'URL de l'API et le modèle sélectionné
    st.markdown(f"Modèle sélectionné : {selected_model}")

enable_5 = st.checkbox("Launch video capturing",key="checkbox_2")

if enable_5:
    image = camera_input_live(key="camera_input_2")

    if image:
        # Image treatment to display back to the user with target rectangle
        bytes_data = image.getvalue()
        input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
        flipped_img = cv2.flip(colored_img, 1)
        annot_img = cv2.rectangle(flipped_img, (X1,Y1), (X2,Y2), (0,255,255), thickness=5, lineType=cv2.LINE_AA)
        st.image(annot_img)

        response = requests.post(f"{url_get_image_prediction_from_gcp_model_5}?model_name={selected_model}", files={"img": image} )

        if response.status_code == 200:
            data = response.json()
            st.success(f"Signe prédit : {data['prediction']}")
            proba = round(max(data['probabilities'][0])*100,2)
            st.success(f"Probabilité : {proba} %")
        else:
            st.error(f"Erreur API : {response.status_code}, {response.text}")




##### FULL CLASSES  #####

st.title("DeepSign — Upload via webcam et OpenCV et predict avec le model GCP Full CLASSES")
st.markdown(f"Working with {url_get_image_prediction_from_gcp_model_full}")


filtered_models_full = [m for m in all_gcp_models if "fullclasses/" in m and m.endswith(".keras")]


if filtered_models_full:

    models_dict = {m.split('/')[-1]: m for m in filtered_models_full}
    selected_model_name  = st.selectbox("Sélectionnez un modèle", list(models_dict.keys()),key="selectbox_3")
    selected_model = models_dict[selected_model_name]

     # Afficher l'URL de l'API et le modèle sélectionné
    st.markdown(f"Modèle sélectionné : {selected_model}")

enable_full = st.checkbox("Launch video capturing",key="checkbox_3")

if enable_full:
    image = camera_input_live(key="camera_input_3")

    if image:
        # Image treatment to display back to the user with target rectangle
        bytes_data = image.getvalue()
        input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
        flipped_img = cv2.flip(colored_img, 1)
        annot_img = cv2.rectangle(flipped_img, (X1,Y1), (X2,Y2), (0,255,255), thickness=5, lineType=cv2.LINE_AA)
        st.image(annot_img)

        response = requests.post(f"{url_get_image_prediction_from_gcp_model_full}?model_name={selected_model}", files={"img": image} )

        if response.status_code == 200:
            data = response.json()
            st.success(f"Signe prédit : {data['prediction']}")
            proba = round(max(data['probabilities'][0])*100,2)
            st.success(f"Probabilité : {proba} %")
        else:
            st.error(f"Erreur API : {response.status_code}, {response.text}")




######################################################
#       OLD
######################################################



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

enable = st.checkbox("Launch video capturing",key="checkbox_1")

if enable:

    image = camera_input_live(key="camera_input_1")

    if image:
        # Image treatment to display back to the user with target rectangle
        bytes_data = image.getvalue()
        input_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        colored_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
        flipped_img = cv2.flip(colored_img, 1)
        annot_img = cv2.rectangle(flipped_img, (X1,Y1), (X2,Y2), (0,255,255), thickness=5, lineType=cv2.LINE_AA)
        st.image(annot_img)

        response = requests.post(url_get_image_prediction, files={"img": image})

        if response.status_code == 200:
            data = response.json()
            st.success(f"Signe prédit : {data['prediction']}")
            proba = round(max(data['probabilities'][0])*100,2)
            st.success(f"Probabilité : {proba} %")
        else:
            st.error(f"Erreur API : {response.status_code}")
