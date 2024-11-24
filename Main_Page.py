import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import os

# Fungsi untuk mengonversi gambar ke Base64


def image_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# Load images

logo_path = os.path.join("image", "logo.jpg")  # Path universal
logo = Image.open(logo_path)
logo_green = os.path.join("image", "logo_white.png")
logo_green = Image.open(logo_green)

# Set page configuration
st.set_page_config(
    page_title="Welcome to NV-Bite!",
    page_icon=logo,
)

# Sidebar success message
st.sidebar.success("Select a demo above.")

# Konversi logo ke Base64 dan tampilkan di tengah
logo_base64 = image_to_base64(logo_green)
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="TechWas Logo" style="width: 50%; max-width: 300px;">
    </div>
    """,
    unsafe_allow_html=True,
)

# Welcome text
st.write(
    "<h1 style='text-align: center;'>Welcome!</h1>",
    unsafe_allow_html=True,
)

# Description
st.markdown(
    """
NV-Bite is a student-led group focused on creating smarter ways to track and reduce food's carbon footprint. Our team of seven, working in machine learning, cloud computing, and mobile development, has built an app to achieve this goal.

This page highlights our app's **Image Classification** and **Generative Text** features. It identifies food items, calculates their carbon footprint, and gives personalized sustainability tips to help users make eco-friendly choices. We want to show how we're using machine learning to encourage eco-friendly food decisions. Your feedback is important to us. Thank you for visiting!    
"""
)

# Link to repository
st.markdown(
    """    
    ##### **Visit our repository [here](https://github.com/NV-Bite)!**
    """
)
