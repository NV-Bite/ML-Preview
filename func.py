import requests
import os
import io
import typing
import json
import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

IMAGE_API_URL = os.getenv("IMAGE_API_URL")
SUMMARIZATION_API_URL = os.getenv("SUMMARIZATION_API_URL")
SUMMARIZATION_TOKEN = os.getenv("SUMMARIZATION_TOKEN")

model = tf.keras.models.load_model("model/Densenet_model.h5")
class_names = [
    "Nasi Padang",
    "Pizza",
    "Soto Ayam"
]


@st.cache_data
def default():
    response = requests.get(IMAGE_API_URL)

    if response.status_code == 200:
        return response.text
    else:
        data = "An error occurred:", response.status_code
        return data


@st.cache_data
def predict(image):
    """This function takes in an image and returns a prediction from an external API.

    Args:
        image (bytes): The image to be used for prediction.

    Returns:
        str: The prediction result.
    """
    url = IMAGE_API_URL + "/predict/"

    payload = {}
    files = {"file": ("image.jpg", io.BytesIO(image), "image/jpeg")}
    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)
    formatted_json = json.dumps(response.json(), indent=4)

    return formatted_json


def preprocess_image(image: Image) -> np.ndarray:
    """Preprocesses an image for prediction.

    Args:
        image (PIL.Image): The image to be preprocessed.

    Returns:
        np.ndarray: The preprocessed image as a numpy array.
    """
    image = image.resize((300, 300))
    image_array = np.array(image)
    image_array = tf.keras.applications.xception.preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)

    return image_array


@st.cache_data
def predict_image(image):
    """Predicts the top 3 classes for an image using a pre-trained model.

    Args:
        image (np.ndarray): An image represented as a NumPy array.

    Returns:
        dict: A dictionary containing the top 3 predicted classes and their probabilities.
    """
    predictions = model.predict(image)
    top_3_indices = np.argsort(predictions)[0, -3:][::-1]

    data_predictions = {}
    for i in top_3_indices:
        data_predictions[class_names[i]] = predictions[0, i] * 100

    return data_predictions


@st.cache_data
def predict_local(uploaded_file):
    start_time = timer()
    pil_image = Image.open(uploaded_file)
    tf_image = preprocess_image(pil_image)
    data_predict = predict_image(tf_image)

    del pil_image, tf_image

    response = {"predictions": data_predict, "time_taken": timer(start_time)}
    formatted_json = json.dumps(response, indent=4)

    return formatted_json


@st.cache_data
def summarize_api(text: str) -> str:
    """This function takes in a text string and returns a summarized version of the text using an external API.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The summarized version of the input text.
    """
    headers = {"Authorization": f"Bearer {SUMMARIZATION_TOKEN}"}

    def query(payload):
        response = requests.post(
            SUMMARIZATION_API_URL, headers=headers, json=payload)
        return response.json()

    output = query(
        {
            "inputs": text,
        }
    )

    return output


@st.cache_data
def timer(start_time: datetime = None) -> "typing.Union[datetime.datetime, str]":
    """
    Measures the time elapsed from a given start time.

    If no start time is provided, returns the current time. If a start time is provided, returns a formatted string
    representing the time elapsed from the start time to the current time.

    Args:
        start_time (datetime.datetime, optional): The start time to measure elapsed time from, or None to get the current time. Defaults to None.

    Returns:
        Union[datetime.datetime, str]: The current time if no start time is provided, or a formatted string representing the elapsed time.
    """
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod(
            (datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        return "%i hours %i minutes and %s seconds." % (
            thour,
            tmin,
            round(tsec, 2),
        )
