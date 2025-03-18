import os
import streamlit as st
import requests

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
