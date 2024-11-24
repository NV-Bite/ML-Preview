import streamlit as st
import func as f
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables from .env file only if not on Streamlit Cloud
load_dotenv()

# Get the API key from st.secrets (if available) or fallback to .env
api_key = os.getenv("API_KEY")

# Check if api_key is available
if not api_key:
    raise ValueError(
        "API Key is not set. Please configure it in .env or Streamlit secrets.")

# Get the API model URL from st.secrets (if available) or fallback to .env
api_model = os.getenv("API_MODEL")

# Check if api_model is available
if not api_model:
    raise ValueError(
        "API Model URL is not set. Please configure it in .env or Streamlit secrets.")

logo = Image.open("image\logo.jpg")
example = Image.open("image\dont_do.png")
img_classlist = Image.open("image\list_class.png")

st.set_page_config(
    page_title="Image Classification",
    page_icon=logo,
)

st.write("# Image Classification Page")

st.markdown(
    """
    On this page, we’ve developed a deep learning model that can recognize 13 different types of objects in images (**see the class list for details**). The model has been trained on a large dataset of images collected from various sources. You can test the model by uploading an image and seeing the predicted class with its confidence score. This page is for users like you to try the model and give feedback, which will help us improve and finalize it before the official release.
    """
)

with st.expander("Example Usage"):
    st.markdown(
        "<h6 style='text-align: center;'>Below is the illustration on how to use this page</h6>\n"
        + "<p style='text-align: center; font-size:80%; '><i>you can use the expander icon to zoom the image (hover the image)</i></p>",
        unsafe_allow_html=True,
    )
    st.image(example, use_column_width=True)

with st.expander("Class list for predictions"):
    st.markdown(
        "<h6 style='text-align: center;'>Below is the class list for predictions</h6>",
        unsafe_allow_html=True,
    )
    st.image(img_classlist)

st.write("---")

st.markdown(
    "<h6 style='text-align: center;'>Predict your own image!</h6>",
    unsafe_allow_html=True,
)

st.write("---")

img_val = None

left_layout, right_layout = st.columns(2)

with left_layout:
    st.write(
        "<h6 style='text-align: center;'>Prediction</h6>",
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Your Image", type=["jpg", "jpeg"], label_visibility="collapsed"
    )
    if uploaded_file:
        img_val = uploaded_file.getvalue()
        print(uploaded_file.name)

with right_layout:
    right_header = st.write(
        "<h6 style='text-align: center;'>Preview</h6>",
        unsafe_allow_html=True,
    )

    if img_val != None:
        st.image(image=img_val, width=300)  # Atur ukuran gambar

st.write("---")

# BUTTON HANDLER
st.session_state.disabled = True
if uploaded_file != None:
    st.session_state.disabled = False

# CENTER BUTTON
_, _, _, mid, _, _, _ = st.columns(7)

with mid:
    solve_button = st.button(
        "Predict!", key="but_solve", disabled=st.session_state.get("disabled")
    )

st.write("")

if solve_button:
    predicted_class, confidence = f.predict(
        img_val)

    st.write(
        f"Predicted class: {predicted_class} with confidence: {confidence}%")
