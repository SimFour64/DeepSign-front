import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from camera_input_live import camera_input_live

st.set_page_config(
    page_title="Capture your sign!", # => Quick reference - Streamlit
    page_icon="🤟",
    layout="wide", # wide
    initial_sidebar_state="auto") # collapsed

"""
# 🎥 Capture your sign and evaluate it!

#### How to use it
    0️⃣ Click on "Start capturing (if needed)
    1️⃣ Do the sign in the blue box
    2️⃣ Click on "Pause capturing"
    3️⃣ Click on "Evaluate!"
"""


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
    # Once user hit "Evaluate" button, the last image is processed to get model input shape
    cropped_img = colored_img[200:500,200:500]
    height = 128
    width = 128
    std_dim = (height, width)
    resized_img = cv2.resize(cropped_img, std_dim)
    c[1].image(resized_img)

    ######################################
    #  PLACEHOLDER: CODE TO SEND TO API  #
    ######################################
    pred = "Hello_test"
    c[1].write(f"Prediction: {pred}")
