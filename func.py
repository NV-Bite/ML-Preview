import requests
import os
import io
from dotenv import load_dotenv
import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np


# Load model
MODEL_PATH = "model/Densenet_model.h5"  # Ganti dengan path model Anda
model = tf.keras.models.load_model(MODEL_PATH)


def load_and_preprocess_image(img_path, target_size=(224, 224)):
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Rescale image
    return img_array


def predict_image(model, img_array, class_labels):
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions)
    predicted_class_label = class_labels[predicted_class_index]
    return predicted_class_label, predictions[0][predicted_class_index]


@st.cache_data
def predict(image):
    # Save the uploaded image to a temporary file
    img_path = "temp_image.jpg"
    with open(img_path, "wb") as f:
        f.write(image)

    # Preprocess the image
    img_array = load_and_preprocess_image(img_path)

    # Define class labels
    # Ganti dengan label kelas Anda
    class_labels = ['nasi padang', 'pizza', 'soto ayam']

    # Predict using the model
    predicted_class, confidence = predict_image(model, img_array, class_labels)

    return {"class": predicted_class, "confidence": confidence}
