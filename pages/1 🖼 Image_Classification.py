import streamlit as st
import func as f
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables from .env file only if not on Streamlit Cloud
if not st.secrets:
    load_dotenv()

# Get the API key from st.secrets (if available) or fallback to .env
api_key = st.secrets.get("API_KEY", os.getenv("API_KEY"))


# Check if api_key is available
if not api_key:
    raise ValueError(
        "API Key is not set. Please configure it in .env or Streamlit secrets.")

# Configure the API key
genai.configure(api_key=api_key)


# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,)
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "sate",
            ],
        },
        {
            "role": "model",
            "parts": [
                "**Makanan:** Sate\n\n**Bahan-bahan:**\n- Daging sapi (non-veg)\n- Bawang merah (veg)\n- Bawang putih (veg)\n- Ketumbar (veg)\n- Jinten (veg)\n- Merica (veg)\n- Kunyit (veg)\n- Jahe (veg)\n- Kecap manis (veg)\n\n**Rincian Emisi Karbon:**\n\n| Bahan | Pertanian | Pengolahan | Transportasi | Ritel | Pengemasan | Kerugian | Penggunaan Lahan |\n|---|---|---|---|---|---|---|---|\n| Daging sapi | 21.92 | 1.55 | 0.59 | 0.25 | 0.37 | 3.85 | 1.27 |\n| Bawang merah | 0.21 | 0.0 | 0.09 | 0.04 | 0.04 | 0.1 | 0.0 |\n| Bawang putih | 0.28 | 0.0 | 0.09 | 0.02 | 0.05 | 0.08 | 0.0 |\n| Ketumbar | 1.58 | 0.41 | 0.13 | 0.05 | 0.11 | 0.47 | 0.49 |\n| Jinten | 3.37 | 0.05 | 0.11 | 0.04 | 0.12 | -0.01 | -3.26 |\n| Merica | 6.69 | 0.33 | 0.11 | 0.04 | 0.72 | 12.94 | 25.81 |\n| Kunyit | 0.49 | 0.79 | 0.18 | 0.27 | 0.18 | 0.29 | 0.96 |\n| Jahe | 0.71 | 0.01 | 0.18 | 0.02 | 0.15 | 0.66 | 0.37 |\n| Kecap manis | - | - | - | - | - | - | - |\n\n**Total Emisi Karbon per Porsi:** 35,42 kg CO2e\n\n**Saran Keberlanjutan:**\n\n* 🌱 Kurangi konsumsi daging sapi, karena merupakan kontributor utama emisi karbon.\n* 🌍 Beli bumbu dan rempah-rempah dari sumber lokal untuk mengurangi emisi transportasi.\n* 🍃 Pilih kecap manis organik yang diproduksi dengan práticas berkelanjutan.\n* ♻️ Gunakan tusuk sate yang dapat digunakan kembali untuk mengurangi kemasan.\n\n**Fakta Keberlanjutan:**\n\n* Produksi daging sapi bertanggung jawab atas sekitar 18% emisi gas rumah kaca global.\n* Mengurangi konsumsi daging adalah salah satu cara paling efektif untuk mengurangi jejak karbon makanan individu.\n\n**Penutupan dengan Kutipan:**\n\n\"Makanan yang kita makan memiliki dampak yang signifikan terhadap lingkungan kita. Dengan membuat pilihan makanan yang berkelanjutan, kita dapat memainkan peran penting dalam mengurangi jejak karbon kita dan melindungi planet ini.\"",
            ],
        },
        {
            "role": "user",
            "parts": [
                "Pizza",
            ],
        },
        {
            "role": "model",
            "parts": [
                "**Makanan:** Pizza\n\n**Bahan-bahan:**\n- Tepung terigu (veg)\n- Saus tomat (veg)\n- Keju (non-veg)\n- Sosis (non-veg)\n- Jamur (veg)\n- Bawang bombay (veg)\n- Paprika (veg)\n- Zaitun (veg)\n\n**Rincian Emisi Karbon:**\n\n| Bahan | Pertanian | Pengolahan | Transportasi | Ritel | Pengemasan | Kerugian | Penggunaan Lahan |\n|---|---|---|---|---|---|---|---|\n| Tepung terigu | 0.82 | 0.21 | 0.13 | 0.06 | 0.09 | 0.18 | 0.1 |\n| Saus tomat | 0.71 | 0.01 | 0.18 | 0.02 | 0.15 | 0.66 | 0.37 |\n| Keju | 13.1 | 0.74 | 0.14 | 0.33 | 0.17 | 2.58 | 4.47 |\n| Sosis | 21.92 | 1.55 | 0.59 | 0.25 | 0.37 | 3.85 | 1.27 |\n| Jamur | 0.49 | 0.79 | 0.18 | 0.27 | 0.18 | 0.29 | 0.96 |\n| Bawang bombay | 0.21 | 0.0 | 0.09 | 0.04 | 0.04 | 0.1 | 0.0 |\n| Paprika | 0.72 | 0.0 | 0.1 | 0.04 | 0.04 | 0.08 | 0.0 |\n| Zaitun | 3.37 | 0.05 | 0.11 | 0.04 | 0.12 | -0.01 | -3.26 |\n\n**Total Emisi Karbon per Porsi (4 potong):** 44,8 kg CO2e\n\n**Saran Keberlanjutan:**\n\n* 🌱 Pilih pizza vegetarian dengan topping sayuran segar seperti jamur, paprika, dan bawang bombay.\n* 🌍 Beli bahan-bahan dari sumber lokal untuk mengurangi emisi transportasi.\n* 🍃 Gunakan tepung organik dan saus tomat yang diproduksi secara berkelanjutan.\n* ♻️ Gunakan kemasan ramah lingkungan untuk sisa pizza.\n\n**Fakta Keberlanjutan:**\n\n* Produksi daging sapi merupakan kontributor utama emisi gas rumah kaca, sehingga mengurangi konsumsi daging dapat secara signifikan mengurangi jejak karbon makanan.\n* Memilih bahan makanan lokal dapat membantu mengurangi emisi transportasi dan mendukung ekonomi lokal.\n\n**Penutupan dengan Kutipan:**\n\n\"Setiap gigitan yang kita ambil mempunyai dampak pada planet kita. Dengan membuat pilihan makanan yang berkelanjutan, kita dapat mengurangi jejak karbon kita dan memastikan masa depan yang lebih berkelanjutan.\"",
            ],
        },
    ]
)


logo = Image.open("image/logo.png")
example = Image.open("image/how-to-demo.png")
img_classlist = Image.open("image/class_list.png")


st.set_page_config(
    page_title="Image Classification",
    page_icon=logo,
)

st.write("# Image Classification Page")

st.markdown(
    """
    In this page, we have developed a deep learning model that can recognize 15 different classes of objects in images (**check class list expander**). Our model is trained on a large and diverse dataset of images collected from various sources. You can try our model yourself by uploading an image. You will see the predicted class and the confidence score of our model. We hope you enjoy exploring our website and learning more about our project.
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
        st.image(image=img_val)

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
    # req to api
    response = f.predict(img_val)

    text = f"**Makanan:** {response['class']}\n\n Anda adalah asisten pintar berbahasa Indonesia yang ahli dalam menghitung jejak karbon dari makanan atau struk makanan dan breakdown bahan bahan pada makanan nya lalu cocokan bahan bahan itu dengan yang ada dalam data emisi yg saya berikan di bawah. Berikut adalah instruksi untuk tugas Anda:**\n\n1. **Identifikasi Makanan**:\n   - Tentukan apakah item makanan bersifat vegetarian atau non-vegetarian.\n   - Buat daftar bahan makanan beserta klasifikasinya (veg/non-veg) yang ada dalam data carbon emisi yg saya berikan saja yg kamu tampilkan.\n\n2. **Rincian Emisi Karbon**:\n   - Hitung emisi karbon berdasarkan faktor seperti pertanian, pengolahan, transportasi, ritel, pengemasan, kerugian, dan penggunaan lahan.\n   -  daftar bahan makana yang ada dalam data carbon emisi yg saya berikan saja yg kamu tampilkan\n\n3. **Rincian Emisi Karbon per Makanan**:\n   - Jika ada beberapa jenis makanan, beri rincian emisi karbon secara terpisah.\n   - Tampilkan total emisi karbon dalam tabel ringkas.\n\n4. **Saran Keberlanjutan**:\n   - Berikan saran terkait keberlanjutan dan pengurangan jejak karbon, seperti:\n     - 🌱 Belilah makanan secukupnya.\n     - 🌍 Pilih produk lokal.\n     - 🍃 Pilih makanan organik.\n     - ♻️ Gunakan kemasan ramah lingkungan.\n\n5. **Fakta Keberlanjutan**:\n   - Sertakan fakta penting tentang jejak karbon makanan (contoh: \"Tahu memiliki jejak karbon 10x lebih rendah daripada daging sapi.\").\n\n6. **Penutupan dengan Kutipan**:\n   - Berikan kutipan yang menginspirasi tentang pentingnya mengurangi jejak karbon makanan untuk perubahan iklim.\n\n**Referensi Data untuk Perhitungan Emisi**:  \nApples: Pertanian 0.23, Pengolahan 0.0, Transportasi 0.1, Ritel 0.02, Pengemasan 0.04, Kerugian 0.07, Penggunaan Lahan -0.03\nBananas: Pertanian 0.27, Pengolahan 0.06, Transportasi 0.3, Ritel 0.02, Pengemasan 0.07, Kerugian 0.18, Penggunaan Lahan -0.03\nBeef: Pertanian 21.92, Pengolahan 1.55, Transportasi 0.59, Ritel 0.25, Pengemasan 0.37, Kerugian 3.85, Penggunaan Lahan 1.27\nBerries & Grapes: Pertanian 0.72, Pengolahan 0.0, Transportasi 0.24, Ritel 0.02, Pengemasan 0.21, Kerugian 0.32, Penggunaan Lahan 0.02\nBrassicas: Pertanian 0.28, Pengolahan 0.0, Transportasi 0.09, Ritel 0.02, Pengemasan 0.05, Kerugian 0.08, Penggunaan Lahan 0.0\nCassava: Pertanian 0.22, Pengolahan 0.0, Transportasi 0.09, Ritel 0.04, Pengemasan 0.04, Kerugian 0.33, Penggunaan Lahan 0.59\nCheese: Pertanian 13.1, Pengolahan 0.74, Transportasi 0.14, Ritel 0.33, Pengemasan 0.17, Kerugian 2.58, Penggunaan Lahan 4.47\nCitrus Fruit: Pertanian 0.31, Pengolahan 0.0, Transportasi 0.09, Ritel 0.02, Pengemasan 0.04, Kerugian 0.07, Penggunaan Lahan -0.15\nCoffee: Pertanian 10.75, Pengolahan 0.61, Transportasi 0.13, Ritel 0.05, Pengemasan 1.69, Kerugian 11.47, Penggunaan Lahan 3.82\nDark Chocolate: Pertanian 6.69, Pengolahan 0.33, Transportasi 0.11, Ritel 0.04, Pengemasan 0.72, Kerugian 12.94, Penggunaan Lahan 25.81\nEggs: Pertanian 1.32, Pengolahan 0.0, Transportasi 0.08, Ritel 0.04, Pengemasan 0.16, Kerugian 0.15, Penggunaan Lahan 0.71\nFish (farmed): Pertanian 8.06, Pengolahan 0.04, Transportasi 0.25, Ritel 0.09, Pengemasan 0.14, Kerugian 2.03, Penggunaan Lahan 1.19\nGroundnuts: Pertanian 1.58, Pengolahan 0.41, Transportasi 0.13, Ritel 0.05, Pengemasan 0.11, Kerugian 0.47, Penggunaan Lahan 0.49\nMilk: Pertanian 1.51, Pengolahan 0.15, Transportasi 0.09, Ritel 0.27, Pengemasan 0.1, Kerugian 0.27, Penggunaan Lahan 0.51\nNuts: Pertanian 3.37, Pengolahan 0.05, Transportasi 0.11, Ritel 0.04, Pengemasan 0.12, Kerugian -0.01, Penggunaan Lahan -3.26\nOatmeal: Pertanian 1.87, Pengolahan 0.06, Transportasi 0.09, Ritel 0.04, Pengemasan 0.09, Kerugian 0.33, Penggunaan Lahan 0.0\nOnions & Leeks: Pertanian 0.21, Pengolahan 0.0, Transportasi 0.09, Ritel 0.04, Pengemasan 0.04, Kerugian 0.1, Penggunaan Lahan 0.0\nOther Fruit: Pertanian 0.37, Pengolahan 0.02, Transportasi 0.18, Ritel 0.02, Pengemasan 0.04, Kerugian 0.3, Penggunaan Lahan 0.13\nOther Vegetables: Pertanian 0.18, Pengolahan 0.06, Transportasi 0.17, Ritel 0.02, Pengemasan 0.04, Kerugian 0.07, Penggunaan Lahan 0.0\nPeas: Pertanian 0.72, Pengolahan 0.0, Transportasi 0.1, Ritel 0.04, Pengemasan 0.04, Kerugian 0.08, Penggunaan Lahan 0.0\nPotatoes: Pertanian 0.19, Pengolahan 0.0, Transportasi 0.09, Ritel 0.04, Pengemasan 0.04, Kerugian 0.09, Penggunaan Lahan 0.0\nRice: Pertanian 3.55, Pengolahan 0.07, Transportasi 0.1, Ritel 0.06, Pengemasan 0.08, Kerugian 0.61, Penggunaan Lahan -0.02\nShrimps (farmed): Pertanian 13.45, Pengolahan 0.0, Transportasi 0.33, Ritel 0.35, Pengemasan 0.54, Kerugian 7.83, Penggunaan Lahan 0.33\nTofu: Pertanian 0.49, Pengolahan 0.79, Transportasi 0.18, Ritel 0.27, Pengemasan 0.18, Kerugian 0.29, Penggunaan Lahan 0.96\nTomatoes: Pertanian 0.71, Pengolahan 0.01, Transportasi 0.18, Ritel 0.02, Pengemasan 0.15, Kerugian 0.66, Penggunaan Lahan 0.37\nWheat & Rye: Pertanian 0.82, Pengolahan 0.21, Transportasi 0.13, Ritel 0.06, Pengemasan 0.09, Kerugian 0.18, Penggunaan Lahan 0.1\nWine: Pertanian 0.63, Pengolahan 0.14, Transportasi 0.09, Ritel 0.04, Pengemasan 0.75, Kerugian 0.2, Penggunaan Lahan -0.06"
    responsegenai = chat_session.send_message(text)

    st.write(
        f"Predicted class: {response['class']} with confidence: {response['confidence']}")
    st.write(responsegenai.text)
