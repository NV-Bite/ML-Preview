import requests
import os
import io
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file only if not on Streamlit Cloud
if not st.secrets:
    load_dotenv()

# Get the API key from st.secrets (if available) or fallback to .env
api_url = st.secrets.get("API_URL", os.getenv("API_URL"))

# Check if api_key is available
if not api_url:
    raise ValueError(
        "API Key is not set. Please configure it in .env or Streamlit secrets.")


@st.cache_data
def default():
    response = requests.get(api_url)

    if response.status_code == 200:
        # data = response.json()
        return response.text
    else:
        data = "An error occurred:", response.status_code
        return data


@st.cache_data
def predict(image):
    url = api_url + "/predict_image"  # Sesuaikan endpoint jika perlu

    # Siapkan file image sesuai dengan format di API
    files = {"image": ("image.jpg", io.BytesIO(image), "image/jpeg")}
    headers = {}

    # Kirim request POST ke API
    response = requests.post(url, headers=headers, files=files)

    # Pastikan bahwa respons dalam format JSON, lalu akses prediksi
    if response.status_code == 200:
        result = response.json()
        predicted_class = result["data"]["predicted_class"]
        confidence = result["data"]["confidence"]

        # Tampilkan hasil prediksi
        return predicted_class, confidence
    else:
        # Tampilkan pesan error jika ada
        return f"Error: {response.status_code} - {response.text}"
