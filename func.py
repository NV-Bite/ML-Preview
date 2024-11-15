import requests
import os
import io
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

if not st.secrets:
    load_dotenv()

# Get the API key from st.secrets (if available) or fallback to .env
api_Url = st.secrets.get("API_URL", os.getenv("API_URL"))


@st.cache_data
def default():
    response = requests.get(api_Url)

    if response.status_code == 200:
        # data = response.json()
        return response.text
    else:
        data = "An error occurred:", response.status_code
        return data


@st.cache_data
def predict(image):
    url = api_Url + "/predict/"

    payload = {}
    files = {"file": ("image.jpg", io.BytesIO(image), "image/jpeg")}
    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    return response.text
