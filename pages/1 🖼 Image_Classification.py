import streamlit as st
import func as f
from PIL import Image
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import json

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_MODEL = st.secrets.get("API_MODEL", os.getenv("API_MODEL"))

print(API_MODEL)


def authenticate():
    # Load credentials from Streamlit secrets
    credentials_info = {
        "type": st.secrets.get["google_drive"]["type"],
        "project_id": st.secrets.get["google_drive"]["project_id"],
        "private_key_id": st.secrets.get["google_drive"]["private_key_id"],
        "private_key": st.secrets.get["google_drive"]["private_key"],
        "client_email": st.secrets.get["google_drive"]["client_email"],
        "client_id": st.secrets.get["google_drive"]["client_id"],
        "auth_uri": st.secrets.get["google_drive"]["auth_uri"],
        "token_uri": st.secrets.get["google_drive"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets.get["google_drive"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets.get["google_drive"]["client_x509_cert_url"]
    }
    creds = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES)
    return creds


def create_folder(service, folder_name, parent_folder_id):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')


def upload_photo(file_path, file_name, folder_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, mimetype='image/jpeg')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"File uploaded to Google Drive with ID: {file.get('id')}")


logo_path = os.path.join("image", "logo.jpg")
logo = Image.open(logo_path)
example = os.path.join("image", "dont_do.png")
example = Image.open(example)
img_classlist = os.path.join("image", "list_class.png")
img_classlist = Image.open(img_classlist)

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
file_name = None

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
        file_name = uploaded_file.name
        print(file_name)

        # Save the uploaded file temporarily
        with open(file_name, "wb") as temp_file:
            temp_file.write(img_val)

with right_layout:
    right_header = st.write(
        "<h6 style='text-align: center;'>Preview</h6>",
        unsafe_allow_html=True,
    )

    if img_val is not None:
        st.image(image=img_val, width=300)  # Atur ukuran gambar

st.write("---")

# BUTTON HANDLER
st.session_state.disabled = True
if uploaded_file is not None:
    st.session_state.disabled = False

# CENTER BUTTON
_, _, _, mid, _, _, _ = st.columns(7)

with mid:
    solve_button = st.button(
        "Predict!", key="but_solve", disabled=st.session_state.get("disabled")
    )

st.write("")

if solve_button and img_val is not None and file_name is not None:
    predicted_class, confidence = f.predict(img_val)
    if predicted_class is not None and confidence is not None:
        st.write(
            f"Predicted class: {predicted_class} with confidence: {confidence}%")

        # Authenticate and create folder if not exists
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)
        folder_id = create_folder(
            service, predicted_class, st.secrets["google_drive"]["folder_id"])

        # Upload the file to Google Drive
        upload_photo(file_name, file_name, folder_id)

        # Remove the temporary file
        os.remove(file_name)
