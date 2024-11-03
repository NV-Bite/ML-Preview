import streamlit as st
from PIL import Image


logo = Image.open("image/logo.png")

st.set_page_config(
    page_title="Welcome!",
)

st.sidebar.success("Select a demo above.")

# st.image(logo_green, use_column_width=True)

st.write(
    "<h1 style='text-align: center;'>Welcome!</h6>",
    unsafe_allow_html=True,
)
