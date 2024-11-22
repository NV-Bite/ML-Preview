import streamlit as st
import google.generativeai as genai
from PIL import Image
from pathlib import Path
from google.api_core.exceptions import InternalServerError
import os
from dotenv import load_dotenv

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


def analyze_image(image_path: str) -> str:
    try:
        # Upload the image file
        myfile = genai.upload_file(Path(image_path))

        # Generate content using the uploaded file
        response = chat_session.send_message(myfile)

        return response.text
    except InternalServerError as e:
        st.error(f"Internal server error: {e.message}")
        return "An error occurred while processing the image."


@st.cache_data
def load_image(image_path):
    return Image.open(image_path)


# Load the logo image
logo = Image.open("image\logo.jpg")

# Set Streamlit page configuration
st.set_page_config(
    page_title="Text Generative",
    page_icon=logo,
)

st.write("# Text Generative Page")

st.markdown(
    """
In this project, we built a Text Generative system that automatically creates answers based on image classification results.

For text generation, we use **Vertex AI’s** services, particularly the Gemini 1.0 Pro language model. This allows us to generate clear and accurate responses that include food identification, carbon emission breakdown, sustainability tips, and relevant facts, providing users with valuable insights into the environmental impact of their food choices.  
"""
)

# Create two columns: left (upload) and right (input text)

# Right column: Input Food Order
st.header("Enter Food Order")
user_input = st.text_area("Enter your food order:", "")
if st.button("Generate Text", key="analyze_button"):
    if user_input:
        try:
            text = f"""**Makanan:** {user_input}\n\n
        Anda adalah asisten pintar berbahasa Indonesia yang ahli dalam menghitung jejak karbon dari makanan atau struk makanan dan breakdown bahan bahan pada makanan nya lalu cocokan bahan bahan itu dengan yang ada dalam data emisi yg saya berikan di bawah. Berikut adalah instruksi untuk tugas Anda:\n\n
        1. **Identifikasi Makanan**:
           - Tentukan apakah item makanan bersifat vegetarian atau non-vegetarian.
           - Buat daftar bahan makanan beserta klasifikasinya (veg/non-veg) yang ada dalam data karbon emisi yg saya berikan saja yg kamu tampilkan.\n\n
        2. **Rincian Emisi Karbon**:
           - Hitung emisi karbon berdasarkan faktor seperti pertanian, pengolahan, transportasi, ritel, pengemasan, kerugian, dan penggunaan lahan.
           - Daftar bahan makanan yang ada dalam data karbon emisi yang saya berikan saja yang kamu tampilkan.\n\n
        3. **Rincian Emisi Karbon per Makanan**:
           - Jika ada beberapa jenis makanan, beri rincian emisi karbon secara terpisah.
           - Tampilkan total emisi karbon dalam tabel ringkas.\n\n
        4. **Saran Keberlanjutan**:
           - Berikan saran terkait keberlanjutan dan pengurangan jejak karbon, seperti:
             - 🌱 Belilah makanan secukupnya.
             - 🌍 Pilih produk lokal.
             - 🍃 Pilih makanan organik.
             - ♻️ Gunakan kemasan ramah lingkungan.\n\n
        5. **Fakta Keberlanjutan**:
           - Sertakan fakta penting tentang jejak karbon makanan (contoh: "Tahu memiliki jejak karbon 10x lebih rendah daripada daging sapi.")\n\n
        6. - Berikan kutipan yang menginspirasi tentang pentingnya mengurangi jejak karbon makanan untuk perubahan iklim.\n\n
        **Referensi Data untuk Perhitungan Emisi**:
        (Data emisi karbon seperti apel, pisang, daging sapi, dsb.)
        """
            # Call the chat session and send the message
            response = chat_session.send_message(user_input)
            # Debug: Display raw response from chat session
            st.write(response.text)
        except InternalServerError as e:
            st.error(f"Internal server error: {e.message}")
    else:
        st.error("Please enter a food order.")
