import requests
import os
import io
# from dotenv import load_dotenv
import streamlit as st

# load_dotenv()

API_URL = st.secrets["API_URL"]
# API_URL = os.getenv("API_URL")


@st.cache_data
def default():
    response = requests.get(API_URL)

    if response.status_code == 200:
        # data = response.json()
        return response.text
    else:
        data = "An error occurred:", response.status_code
        return data


@st.cache_data
def predict(image):
    url = API_URL + "/predict/"

    payload = {}
    files = {"file": ("image.jpg", io.BytesIO(image), "image/jpeg")}
    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    return response.text
