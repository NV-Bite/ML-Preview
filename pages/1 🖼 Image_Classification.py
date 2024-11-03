import streamlit as st
# import func as f
from PIL import Image


@st.cache_data
def load_image(image_path):
    return Image.open(image_path)


logo = Image.open("image/logo.png")

st.set_page_config(
    page_title="Image Classification",
    page_icon=logo,
)

st.write(
    "<h1 style='text-align: center;'>Ongoing!</h6>",
    unsafe_allow_html=True,
)


# st.markdown(
#     """
#     In this page, we have developed a deep learning model that can recognize 15 different classes of objects in images (**check class list expander**). Our model is trained on a large and diverse dataset of images collected from various sources. You can try our model yourself by uploading an image. You will see the predicted class and the confidence score of our model. We hope you enjoy exploring our website and learning more about our project.
#     """
# )

# with st.expander("Example Usage"):
#     st.markdown(
#         "<h6 style='text-align: center;'>Below is the illustration on how to use this page</h6>\n"
#         + "<p style='text-align: center; font-size:80%; '><i>you can use the expander icon to zoom the image (hover the image)</i></p>",
#         unsafe_allow_html=True,
#     )
#     st.image(example, use_column_width=True)

# with st.expander("Class list for predictions"):
#     st.markdown(
#         "<h6 style='text-align: center;'>Below is the class list for predictions</h6>",
#         unsafe_allow_html=True,
#     )
#     st.image(img_classlist)

# st.write("---")

# st.markdown(
#     "<h6 style='text-align: center;'>Predict your own image!</h6>",
#     unsafe_allow_html=True,
# )

# st.write("---")

# img_val = None

# left_layout, right_layout = st.columns(2)

# with left_layout:
#     st.write(
#         "<h6 style='text-align: center;'>Prediction</h6>",
#         unsafe_allow_html=True,
#     )
#     uploaded_file = st.file_uploader(
#         "Your Image", type=["jpg", "jpeg"], label_visibility="collapsed"
#     )
#     if uploaded_file:
#         img_val = uploaded_file.getvalue()
#         print(uploaded_file.name)

# with right_layout:
#     right_header = st.write(
#         "<h6 style='text-align: center;'>Preview</h6>",
#         unsafe_allow_html=True,
#     )

#     if img_val != None:
#         st.image(image=img_val)

#     # contains response
#     # response = ...

# st.write("---")

# # BUTTON HANDLER
# st.session_state.disabled = True
# if uploaded_file != None:
#     st.session_state.disabled = False

# # CENTER BUTTON
# _, _, _, mid, _, _, _ = st.columns(7)

# with mid:
#     solve_button = st.button(
#         "Predict!", key="but_solve", disabled=st.session_state.get("disabled")
#     )

# st.write("")

# if solve_button:
#     # req to api
#     response = f.predict(img_val)
#     st.code(response)
