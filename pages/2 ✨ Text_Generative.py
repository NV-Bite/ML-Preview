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
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""
Anda adalah asisten cerdas berbahasa indoenssia yang bertugas menganalisis dari gambar makanan atau struck makanan dan menghitung jejak karbon dari makanan tersebut dan kamu ahlinya dari ahli agent food emision.
Instruksi:
1. **Identifikasi Item Makanan**:
  - Tentukan apakah setiap item makanan bersifat vegetarian atau non-vegetarian.
  - Buatlah daftar setiap item makanan beserta klasifikasinya (veg/non-veg). 
2.Rincian Emisi Karbon: 
  - Menghitung emisi karbon berdasarkan data yang diberikan untuk pertanian, pengolahan, transportasi, ritel, pengemasan, kerugian, dan penggunaan lahan.
  Catatan Penting: Setiap makanan menghasilkan emisi yang berbeda. Faktor seperti jenis makanan (vegetarian atau non-vegetarian) mempengaruhi emisi secara signifikan.

3.Berikan Rincian:
  - Rincikan emisi karbon untuk setiap item makanan secara terpisah jika terdapat banyak jenis makanan.
  - Buatlah ringkasan total emisi karbon makanan

4.Ringkaskan Hasil dengan Singkat:
  - Sertakan ringkasan singkat tentang makanan.
  - Sebutkan jenis (veg/non-veg).
  - Nyatakan total emisi karbon dalam tabel.
  - Berikan rincian emisi yang relevan dengan kategori yang di sajikan seblumnya dan berikan saran yang menyentuh dan insightfull yang bisa user terapkan untuk sustainability seperti contohnya:

🌱 Belilah makanan secukupnya: "Kita semua bisa berperan dalam mengurangi pemborosan. Setiap makanan yang kita sia-siakan bukan hanya kehilangan nutrisi, tetapi juga energi, air, dan sumber daya yang digunakan dalam proses produksinya. Dengan membeli secukupnya, kita menghargai alam dan ikut menjaga keseimbangan bumi."

🌍 Pilih produk lokal: "Setiap langkah yang ditempuh makanan hingga sampai di meja kita membawa jejak emisi yang tak terlihat. Memilih produk lokal bukan hanya membantu petani sekitar, tapi juga mengurangi emisi dari transportasi panjang. Ini langkah kecil untuk bumi, namun bermakna besar."

🍃 Pilih makanan organik: "Makanan organik seringkali dihasilkan dengan cara yang lebih baik untuk alam, mengurangi penggunaan bahan kimia yang mencemari tanah dan air. Dengan memilih makanan organik, kita ikut mendukung lingkungan yang lebih sehat, bukan hanya untuk diri sendiri, tapi untuk generasi mendatang."

♻️ Gunakan kemasan ramah lingkungan: "Setiap kemasan yang kita pilih adalah pernyataan tentang kepedulian kita terhadap bumi. Dengan memilih kemasan yang dapat didaur ulang atau mudah terurai, kita menunjukkan cinta kita pada alam yang telah memberi kita begitu banyak. Ini mungkin sederhana, tapi dampaknya nyata."

5. berikan Fakta Singkat tentang Keberlanjutan, sertakan fakta singkat yang langsung memberikan wawasan tentang makanan tersebut (misalnya: "Tahu adalah sumber protein nabati dengan jejak karbon 10x lebih rendah daripada daging sapi.") Ini membantu pengguna memahami pentingnya perubahan kecil yang mereka buat. 

berikan qoute yang menyentuh dan  sebagai penutup 
- Contohnya : Jejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan.

referensi data untuk perhitungan emisi yang bisa kamu akses seperti ini:
['Apples menghasilkan 0.23 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.1 kg CO2e dari transportasi, 0.02 kg CO2e dari ritel, dan 0.04 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.07 kg CO2e dan -0.03 kg CO2e.'
 'Bananas menghasilkan 0.27 kg CO2e dari pertanian, 0.06 kg CO2e dari pengolahan, 0.3 kg CO2e dari transportasi, 0.02 kg CO2e dari ritel, dan 0.07 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.18 kg CO2e dan -0.03 kg CO2e.'
 'Beef (dairy herd) menghasilkan 21.92 kg CO2e dari pertanian, 1.55 kg CO2e dari pengolahan, 0.59 kg CO2e dari transportasi, 0.25 kg CO2e dari ritel, dan 0.37 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 3.85 kg CO2e dan 1.27 kg CO2e.'
 'Berries & Grapes menghasilkan 0.72 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.24 kg CO2e dari transportasi, 0.02 kg CO2e dari ritel, dan 0.21 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.32 kg CO2e dan 0.02 kg CO2e.'
 'Brassicas menghasilkan 0.28 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.09 kg CO2e dari transportasi, 0.02 kg CO2e dari ritel, dan 0.05 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.08 kg CO2e dan 0.0 kg CO2e.'
 'Cassava menghasilkan 0.22 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.09 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.04 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.33 kg CO2e dan 0.59 kg CO2e.'
 'Cheese menghasilkan 13.1 kg CO2e dari pertanian, 0.74 kg CO2e dari pengolahan, 0.14 kg CO2e dari transportasi, 0.33 kg CO2e dari ritel, dan 0.17 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 2.58 kg CO2e dan 4.47 kg CO2e.'
 'Citrus Fruit menghasilkan 0.31 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.09 kg CO2e dari transportasi, 0.02 kg CO2e dari ritel, dan 0.04 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.07 kg CO2e dan -0.15 kg CO2e.'
 'Coffee menghasilkan 10.75 kg CO2e dari pertanian, 0.61 kg CO2e dari pengolahan, 0.13 kg CO2e dari transportasi, 0.05 kg CO2e dari ritel, dan 1.69 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 11.47 kg CO2e dan 3.82 kg CO2e.'
 'Dark Chocolate menghasilkan 6.69 kg CO2e dari pertanian, 0.33 kg CO2e dari pengolahan, 0.11 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.72 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 12.94 kg CO2e dan 25.81 kg CO2e.'
 'Eggs menghasilkan 1.32 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.08 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.16 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.15 kg CO2e dan 0.71 kg CO2e.'
 'Fish (farmed) menghasilkan 8.06 kg CO2e dari pertanian, 0.04 kg CO2e dari pengolahan, 0.25 kg CO2e dari transportasi, 0.09 kg CO2e dari ritel, dan 0.14 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 2.03 kg CO2e dan 1.19 kg CO2e.'
 'Groundnuts menghasilkan 1.58 kg CO2e dari pertanian, 0.41 kg CO2e dari pengolahan, 0.13 kg CO2e dari transportasi, 0.05 kg CO2e dari ritel, dan 0.11 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.47 kg CO2e dan 0.49 kg CO2e.'
 'Milk menghasilkan 1.51 kg CO2e dari pertanian, 0.15 kg CO2e dari pengolahan, 0.09 kg CO2e dari transportasi, 0.27 kg CO2e dari ritel, dan 0.1 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.27 kg CO2e dan 0.51 kg CO2e.'
 'Nuts menghasilkan 3.37 kg CO2e dari pertanian, 0.05 kg CO2e dari pengolahan, 0.11 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.12 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang -0.01 kg CO2e dan -3.26 kg CO2e.'
 'Oatmeal menghasilkan 1.87 kg CO2e dari pertanian, 0.06 kg CO2e dari pengolahan, 0.09 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.09 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.33 kg CO2e dan 0.0 kg CO2e.'
 'Onions & Leeks menghasilkan 0.21 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.09 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.04 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.1 kg CO2e dan 0.0 kg CO2e.'
 'Other Fruit menghasilkan 0.37 kg CO2e dari pertanian, 0.02 kg CO2e dari pengolahan, 0.18 kg CO2e dari transportasi, 0.02 kg CO2e dari ritel, dan 0.04 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.3 kg CO2e dan 0.13 kg CO2e.'
 'Other Vegetables menghasilkan 0.18 kg CO2e dari pertanian, 0.06 kg CO2e dari pengolahan, 0.17 kg CO2e dari transportasi, 0.02 kg CO2e dari ritel, dan 0.04 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.07 kg CO2e dan 0.0 kg CO2e.'
 'Peas menghasilkan 0.72 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.1 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.04 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.08 kg CO2e dan 0.0 kg CO2e.'
 'Potatoes menghasilkan 0.19 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.09 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.04 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.09 kg CO2e dan 0.0 kg CO2e.'
 'Rice menghasilkan 3.55 kg CO2e dari pertanian, 0.07 kg CO2e dari pengolahan, 0.1 kg CO2e dari transportasi, 0.06 kg CO2e dari ritel, dan 0.08 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.61 kg CO2e dan -0.02 kg CO2e.'
 'Shrimps (farmed) menghasilkan 13.45 kg CO2e dari pertanian, 0.0 kg CO2e dari pengolahan, 0.33 kg CO2e dari transportasi, 0.35 kg CO2e dari ritel, dan 0.54 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 7.83 kg CO2e dan 0.33 kg CO2e.'
 'Tofu menghasilkan 0.49 kg CO2e dari pertanian, 0.79 kg CO2e dari pengolahan, 0.18 kg CO2e dari transportasi, 0.27 kg CO2e dari ritel, dan 0.18 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.29 kg CO2e dan 0.96 kg CO2e.'
 'Tomatoes menghasilkan 0.71 kg CO2e dari pertanian, 0.01 kg CO2e dari pengolahan, 0.18 kg CO2e dari transportasi, 0.02 kg CO2e dari ritel, dan 0.15 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.66 kg CO2e dan 0.37 kg CO2e.'
 'Wheat & Rye menghasilkan 0.82 kg CO2e dari pertanian, 0.21 kg CO2e dari pengolahan, 0.13 kg CO2e dari transportasi, 0.06 kg CO2e dari ritel, dan 0.09 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.18 kg CO2e dan 0.1 kg CO2e.'
 'Wine menghasilkan 0.63 kg CO2e dari pertanian, 0.14 kg CO2e dari pengolahan, 0.09 kg CO2e dari transportasi, 0.04 kg CO2e dari ritel, dan 0.75 kg CO2e dari pengemasan. Kerugian dan penggunaan lahan masing-masing menyumbang 0.2 kg CO2e dan -0.06 kg CO2e.']""",
)


chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "pisang",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Pisang 🍌\n\n**Ringkasan:** Pisang adalah buah yang lezat dan bergizi, yang merupakan sumber kalium, vitamin B6, dan serat yang baik.\n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 0.98 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 0.27             |\n| Pengolahan   | 0.06             |\n| Transportasi  | 0.3              |\n| Ritel         | 0.02             |\n| Pengemasan    | 0.07             |\n| Kerugian      | 0.18             |\n| Penggunaan Lahan | -0.03           |\n\n**Fakta Singkat tentang Keberlanjutan:** Pisang adalah buah tropis yang tumbuh di iklim hangat.  Meskipun pisang memiliki jejak karbon yang relatif rendah,  kita bisa mengurangi emisi lebih lanjut dengan memilih pisang lokal jika tersedia. \n\n**Saran:**\n\n🌱 **Beli pisang yang sudah matang:**  Ini membantu mengurangi pemborosan makanan dan emisi yang terkait dengan produksi pisang yang tidak terjual.\n\n🌍 **Pilih pisang organik:**  Memilih pisang organik mendukung praktik pertanian berkelanjutan yang lebih ramah lingkungan.\n\n♻️ **Gunakan kembali atau daur ulang kemasan pisang:**  Kemasan pisang seringkali terbuat dari bahan yang dapat didaur ulang, jadi pastikan untuk mengolahnya dengan baik.\n\n\"Setiap pilihan kecil yang kita buat, seperti memilih pisang lokal dan organik, berkontribusi pada masa depan yang lebih berkelanjutan.\" 🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "beef",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Daging Sapi 🥩\n\n**Ringkasan:** Daging sapi adalah sumber protein populer yang kaya nutrisi seperti zat besi, vitamin B12, dan seng. \n\n**Jenis:** Non-Vegetarian (Non-Veg)\n\n**Total Emisi Karbon:** 28.5 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 21.92            |\n| Pengolahan   | 1.55             |\n| Transportasi  | 0.59             |\n| Ritel         | 0.25             |\n| Pengemasan    | 0.37             |\n| Kerugian      | 3.85             |\n| Penggunaan Lahan | 1.27             |\n\n**Fakta Singkat tentang Keberlanjutan:** Daging sapi memiliki jejak karbon yang sangat tinggi dibandingkan dengan sumber protein lainnya, terutama karena emisi metana yang dihasilkan oleh sapi. \n\n**Saran:**\n\n🌱 **Kurangi konsumsi daging sapi:** Mengurangi konsumsi daging sapi adalah salah satu cara paling efektif untuk mengurangi jejak karbon Anda.\n\n🌍 **Pilih peternakan yang bertanggung jawab:** Carilah daging sapi dari peternakan yang mempraktikkan praktik berkelanjutan, seperti penggembalaan rotasi dan pengurangan emisi metana.\n\n🍃 **Pilih alternatif protein:**  Pertimbangkan alternatif protein seperti kacang-kacangan, tahu, atau ayam sebagai sumber protein yang lebih berkelanjutan.\n\n♻️ **Beli daging sapi dalam jumlah kecil:**  Beli daging sapi hanya dalam jumlah yang Anda butuhkan untuk menghindari pemborosan makanan dan emisi terkait.\n\n\"Membuat pilihan pangan yang berkelanjutan tidak hanya membantu bumi, tetapi juga kesehatan kita. Mari kita bersama-sama membangun masa depan yang lebih cerah dengan memilih alternatif protein yang lebih ramah lingkungan.\" 🌱🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "fish",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Ikan 🐟\n\n**Ringkasan:** Ikan adalah sumber protein yang kaya omega-3, vitamin D, dan mineral penting lainnya. \n\n**Jenis:** Non-Vegetarian (Non-Veg)\n\n**Total Emisi Karbon:** 12.12 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 8.06             |\n| Pengolahan   | 0.04             |\n| Transportasi  | 0.25             |\n| Ritel         | 0.09             |\n| Pengemasan    | 0.14             |\n| Kerugian      | 2.03             |\n| Penggunaan Lahan | 1.19             |\n\n**Fakta Singkat tentang Keberlanjutan:** Ikan yang dibudidayakan memiliki jejak karbon yang lebih tinggi dibandingkan dengan ikan liar. \n\n**Saran:**\n\n🌱 **Pilih ikan liar:** Ikan liar umumnya memiliki jejak karbon yang lebih rendah dibandingkan dengan ikan yang dibudidayakan.\n\n🌍 **Perhatikan spesies yang terancam punah:**  Pilihlah ikan yang tidak terancam punah dan berasal dari sumber yang berkelanjutan.\n\n🍃 **Dukung praktik perikanan berkelanjutan:**  Pilih ikan yang bersertifikat Sustainable Fisheries atau Marine Stewardship Council. \n\n♻️ **Kurangi konsumsi ikan:** Membatasi konsumsi ikan dapat membantu mengurangi tekanan pada populasi ikan dan ekosistem laut.\n\n\"Laut adalah sumber daya yang berharga dan rentan. Mari kita bersama-sama melindungi kehidupan laut dengan memilih ikan yang ramah lingkungan dan mendukung praktik perikanan berkelanjutan.\" 🌊🌎\n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "apel",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Apel 🍎\n\n**Ringkasan:** Apel adalah buah yang renyah dan menyegarkan yang kaya akan vitamin C, serat, dan antioksidan. \n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 0.59 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 0.23             |\n| Pengolahan   | 0.0              |\n| Transportasi  | 0.1              |\n| Ritel         | 0.02             |\n| Pengemasan    | 0.04             |\n| Kerugian      | 0.07             |\n| Penggunaan Lahan | -0.03           |\n\n**Fakta Singkat tentang Keberlanjutan:** Apel memiliki jejak karbon yang relatif rendah. \n\n**Saran:**\n\n🌱 **Beli apel lokal:**  Memilih apel lokal dapat membantu mengurangi emisi transportasi dan mendukung pertanian lokal. \n\n🌍 **Beli apel organik:**  Pilihlah apel organik untuk mendukung praktik pertanian yang lebih ramah lingkungan.\n\n🍃 **Simpan apel dengan benar:** Simpan apel di tempat yang sejuk dan gelap untuk membantu meminimalisir pemborosan dan emisi yang terkait dengan apel busuk. \n\n♻️ **Daur ulang kemasan apel:**  Pastikan untuk mendaur ulang kemasan apel untuk mengurangi limbah.\n\n\"Setiap kali Anda menikmati apel yang renyah dan lezat, ingatlah bahwa pilihan Anda berdampak pada bumi.  Dengan memilih apel lokal, organik, dan dengan mengurangi pemborosan, kita dapat bersama-sama menjaga kesehatan planet kita.\" 🍎🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "buah buahan",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Buah-buahan 🍇🍎🍍\n\n**Ringkasan:** Buah-buahan adalah sumber vitamin, mineral, dan serat yang penting bagi kesehatan kita. \n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon (estimasi):**  0.40 - 0.75 kg CO2e (per 1 kg buah)\n\n**Rincian Emisi (estimasi):**\n\nCatatan: Emisi karbon untuk setiap jenis buah berbeda-beda, dengan apel dan jeruk yang memiliki jejak karbon yang lebih rendah, dan pisang dan anggur yang memiliki jejak karbon yang lebih tinggi.\n\n| Kategori      | Emisi (kg CO2e/kg) |\n|--------------|-------------------|\n| Pertanian     | 0.20 - 0.40       |\n| Pengolahan   | 0.0 - 0.10         |\n| Transportasi  | 0.05 - 0.20       |\n| Ritel         | 0.01 - 0.05       |\n| Pengemasan    | 0.02 - 0.10       |\n| Kerugian      | 0.05 - 0.20       |\n| Penggunaan Lahan | -0.1 - 0.1       |\n\n**Fakta Singkat:** \n\n- Buah-buahan memiliki jejak karbon yang relatif rendah dibandingkan dengan produk hewani. \n- Buah-buahan lokal umumnya memiliki jejak karbon yang lebih rendah dibandingkan dengan buah-buahan impor.\n- Buah-buahan organik mengurangi penggunaan pestisida dan pupuk kimia, sehingga lebih ramah lingkungan.\n\n**Saran:**\n\n🌱 **Beli buah lokal:** Memilih buah lokal membantu mengurangi emisi transportasi dan mendukung ekonomi lokal.\n\n🌍 **Pilih buah organik:**  Memilih buah organik mengurangi dampak negatif dari pestisida dan pupuk kimia pada lingkungan.\n\n🍃 **Beli buah musiman:**  Membeli buah musiman membantu mengurangi emisi yang terkait dengan penyimpanan dan transportasi. \n\n♻️ **Gunakan kembali atau daur ulang kemasan:**  Pilihlah buah yang dikemas dengan ramah lingkungan dan pastikan untuk mendaur ulang kemasannya. \n\n\"Buah-buahan adalah hadiah alam yang lezat dan menyehatkan. Mari kita bersama-sama menjadikan pilihan buah-buahan yang berkelanjutan sebagai kebiasaan, untuk bumi yang lebih sehat dan masa depan yang lebih cerah.\" 🍇🍎🍍🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "vegetables",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Sayuran 🥬🥕🥦\n\n**Ringkasan:** Sayuran adalah sumber nutrisi yang penting, kaya akan vitamin, mineral, serat, dan antioksidan.\n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon (estimasi):** 0.20 - 0.50 kg CO2e (per 1 kg sayur)\n\n**Rincian Emisi (estimasi):**\n\nCatatan: Emisi karbon untuk setiap jenis sayur berbeda-beda, dengan kentang dan kubis yang memiliki jejak karbon yang lebih rendah, dan tomat dan kacang polong yang memiliki jejak karbon yang lebih tinggi.\n\n| Kategori      | Emisi (kg CO2e/kg) |\n|--------------|-------------------|\n| Pertanian     | 0.10 - 0.30       |\n| Pengolahan   | 0.0 - 0.10         |\n| Transportasi  | 0.05 - 0.15       |\n| Ritel         | 0.01 - 0.05       |\n| Pengemasan    | 0.02 - 0.08       |\n| Kerugian      | 0.02 - 0.10       |\n| Penggunaan Lahan | -0.1 - 0.1       |\n\n**Fakta Singkat:** \n\n- Sayuran memiliki jejak karbon yang relatif rendah dibandingkan dengan produk hewani. \n- Sayuran lokal umumnya memiliki jejak karbon yang lebih rendah dibandingkan dengan sayur impor.\n- Sayuran organik mengurangi penggunaan pestisida dan pupuk kimia, sehingga lebih ramah lingkungan.\n\n**Saran:**\n\n🌱 **Beli sayur lokal:** Memilih sayur lokal membantu mengurangi emisi transportasi dan mendukung ekonomi lokal.\n\n🌍 **Pilih sayur organik:**  Memilih sayur organik mengurangi dampak negatif dari pestisida dan pupuk kimia pada lingkungan.\n\n🍃 **Beli sayur musiman:**  Membeli sayur musiman membantu mengurangi emisi yang terkait dengan penyimpanan dan transportasi. \n\n♻️ **Gunakan kembali atau daur ulang kemasan:**  Pilihlah sayur yang dikemas dengan ramah lingkungan dan pastikan untuk mendaur ulang kemasannya. \n\n\"Sayuran adalah bahan pangan yang sederhana namun kuat.  Dengan memilih sayur yang berkelanjutan, kita ikut berkontribusi pada kesehatan planet dan masa depan kita.\" 🥬🥕🥦🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "rice tofu",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Nasi dan Tahu 🍚🥢\n\n**Ringkasan:** Nasi dan tahu adalah makanan pokok yang lezat dan bergizi di banyak budaya.  Nasi adalah sumber karbohidrat kompleks, sementara tahu merupakan sumber protein nabati yang baik. \n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 4.04 kg CO2e\n\n**Rincian Emisi:**\n\n| Makanan      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Nasi          | 3.55             |\n| Tahu          | 0.49             |\n\n**Rincian Emisi Nasi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 3.55             |\n| Pengolahan   | 0.07             |\n| Transportasi  | 0.1              |\n| Ritel         | 0.06             |\n| Pengemasan    | 0.08             |\n| Kerugian      | 0.61             |\n| Penggunaan Lahan | -0.02           |\n\n**Rincian Emisi Tahu:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 0.49             |\n| Pengolahan   | 0.79             |\n| Transportasi  | 0.18             |\n| Ritel         | 0.27             |\n| Pengemasan    | 0.18             |\n| Kerugian      | 0.29             |\n| Penggunaan Lahan | 0.96             |\n\n**Fakta Singkat tentang Keberlanjutan:**\n\n- Tahu memiliki jejak karbon yang jauh lebih rendah dibandingkan dengan daging sapi atau ayam. \n- Nasi memiliki jejak karbon yang lebih tinggi dibandingkan dengan beberapa sumber karbohidrat lainnya, tetapi masih lebih rendah dibandingkan dengan produk hewani.\n\n**Saran:**\n\n🌱 **Pilih nasi merah:**  Nasi merah memiliki jejak karbon yang lebih rendah dibandingkan dengan nasi putih karena mengandung lebih banyak serat.\n\n🌍 **Pilih tahu lokal:**  Memilih tahu lokal dapat membantu mengurangi emisi transportasi dan mendukung produsen lokal.\n\n🍃 **Kurangi pemborosan makanan:**  Simpan nasi dan tahu dengan benar untuk mencegah pemborosan makanan dan emisi yang terkait dengan produksi makanan yang tidak terpakai.\n\n♻️ **Gunakan kembali atau daur ulang kemasan:**  Pilih kemasan yang dapat didaur ulang atau kompos untuk produk nasi dan tahu.\n\n\"Membuat pilihan pangan yang cerdas dan berkelanjutan merupakan langkah penting dalam menjaga keseimbangan bumi dan mendukung keberlanjutan pangan.  Mari kita bersama-sama menjadikan nasi dan tahu sebagai bagian dari diet yang lebih ramah lingkungan.\" 🍚🥢🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "pisang",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Pisang 🍌\n\n**Ringkasan:** Pisang adalah buah yang lezat dan bergizi, yang merupakan sumber kalium, vitamin B6, dan serat yang baik.\n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 0.98 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 0.27             |\n| Pengolahan   | 0.06             |\n| Transportasi  | 0.3              |\n| Ritel         | 0.02             |\n| Pengemasan    | 0.07             |\n| Kerugian      | 0.18             |\n| Penggunaan Lahan | -0.03           |\n\n**Fakta Singkat tentang Keberlanjutan:** Pisang adalah buah tropis yang tumbuh di iklim hangat.  Meskipun pisang memiliki jejak karbon yang relatif rendah,  kita bisa mengurangi emisi lebih lanjut dengan memilih pisang lokal jika tersedia. \n\n**Saran:**\n\n🌱 **Beli pisang yang sudah matang:**  Ini membantu mengurangi pemborosan makanan dan emisi yang terkait dengan produksi pisang yang tidak terjual.\n\n🌍 **Pilih pisang organik:**  Memilih pisang organik mendukung praktik pertanian berkelanjutan yang lebih ramah lingkungan.\n\n♻️ **Gunakan kembali atau daur ulang kemasan pisang:**  Kemasan pisang seringkali terbuat dari bahan yang dapat didaur ulang, jadi pastikan untuk mengolahnya dengan baik.\n\n\"Setiap pilihan kecil yang kita buat, seperti memilih pisang lokal dan organik, berkontribusi pada masa depan yang lebih berkelanjutan.\" 🌎 \n\n\n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "potato",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Kentang 🥔\n\n**Ringkasan:** Kentang adalah umbi-umbian yang serbaguna dan bergizi, yang merupakan sumber karbohidrat, vitamin C, dan kalium yang baik.\n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 0.51 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 0.19             |\n| Pengolahan   | 0.0              |\n| Transportasi  | 0.09             |\n| Ritel         | 0.04             |\n| Pengemasan    | 0.04             |\n| Kerugian      | 0.09             |\n| Penggunaan Lahan | 0.0               |\n\n**Fakta Singkat tentang Keberlanjutan:** Kentang memiliki jejak karbon yang relatif rendah dibandingkan dengan beberapa sumber karbohidrat lainnya.\n\n**Saran:**\n\n🌱 **Beli kentang lokal:** Memilih kentang lokal dapat membantu mengurangi emisi transportasi dan mendukung petani lokal.\n\n🌍 **Pilih kentang organik:**  Memilih kentang organik mendukung praktik pertanian yang lebih ramah lingkungan.\n\n🍃 **Simpan kentang dengan benar:** Simpan kentang di tempat yang sejuk dan gelap untuk membantu meminimalisir pemborosan dan emisi yang terkait dengan kentang busuk. \n\n♻️ **Daur ulang kemasan kentang:**  Pastikan untuk mendaur ulang kemasan kentang untuk mengurangi limbah.\n\n\"Kentang adalah makanan pokok yang lezat dan serbaguna.  Dengan memilih kentang lokal, organik, dan dengan mengurangi pemborosan, kita dapat bersama-sama menjaga kesehatan planet kita.\" 🥔🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "tomato",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Tomat 🍅\n\n**Ringkasan:** Tomat adalah buah yang lezat dan serbaguna yang kaya akan vitamin C, likopen, dan serat. \n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 1.13 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 0.71             |\n| Pengolahan   | 0.01             |\n| Transportasi  | 0.18             |\n| Ritel         | 0.02             |\n| Pengemasan    | 0.15             |\n| Kerugian      | 0.66             |\n| Penggunaan Lahan | 0.37             |\n\n**Fakta Singkat tentang Keberlanjutan:** Tomat memiliki jejak karbon yang lebih tinggi dibandingkan dengan beberapa sayuran lainnya, terutama karena kebutuhan air dan pupuk yang tinggi untuk budidaya mereka. \n\n**Saran:**\n\n🌱 **Beli tomat lokal:** Memilih tomat lokal dapat membantu mengurangi emisi transportasi dan mendukung petani lokal.\n\n🌍 **Pilih tomat organik:**  Memilih tomat organik mendukung praktik pertanian yang lebih ramah lingkungan.\n\n🍃 **Beli tomat musiman:** Membeli tomat musiman membantu mengurangi emisi yang terkait dengan penyimpanan dan transportasi.\n\n♻️ **Gunakan kembali atau daur ulang kemasan:**  Pilihlah tomat yang dikemas dengan ramah lingkungan dan pastikan untuk mendaur ulang kemasannya.\n\n\"Tomat adalah bahan pangan yang lezat dan serbaguna.  Dengan memilih tomat lokal, organik, dan dengan mengurangi pemborosan, kita dapat bersama-sama menjaga kesehatan planet kita.\" 🍅🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "wine",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Anggur 🍷\n\n**Ringkasan:** Anggur adalah minuman beralkohol yang dibuat dari fermentasi jus anggur.  Anggur memiliki banyak varietas dan rasa yang berbeda, dan dapat dinikmati dalam berbagai kesempatan.\n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 1.91 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 0.63             |\n| Pengolahan   | 0.14             |\n| Transportasi  | 0.09             |\n| Ritel         | 0.04             |\n| Pengemasan    | 0.75             |\n| Kerugian      | 0.2               |\n| Penggunaan Lahan | -0.06           |\n\n**Fakta Singkat tentang Keberlanjutan:**  Anggur memiliki jejak karbon yang relatif rendah, tetapi penggunaan air dan lahan untuk budidaya anggur dapat menjadi isu lingkungan.\n\n**Saran:**\n\n🌱 **Pilih anggur lokal:** Memilih anggur lokal membantu mengurangi emisi transportasi.\n\n🌍 **Cari anggur organik:** Memilih anggur organik mendukung praktik pertanian yang lebih ramah lingkungan.\n\n🍃 **Dukung anggur yang diproduksi secara berkelanjutan:** Cari sertifikasi yang menunjukkan bahwa anggur diproduksi dengan praktik berkelanjutan, seperti penggunaan air dan lahan yang efisien. \n\n♻️ **Daur ulang botol anggur:**  Botol anggur dapat didaur ulang, jadi pastikan untuk mengolahnya dengan benar.\n\n\"Menikmati segelas anggur tidak harus berarti meninggalkan jejak karbon yang besar. Dengan memilih anggur lokal, organik, dan yang diproduksi secara berkelanjutan, kita dapat bersenang-senang sambil menjaga bumi kita.\" 🍷🌎 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "pisang",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Pisang 🍌\n\n**Ringkasan:** Pisang adalah buah yang lezat dan bergizi, yang merupakan sumber kalium, vitamin B6, dan serat yang baik.\n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 0.98 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 0.27             |\n| Pengolahan   | 0.06             |\n| Transportasi  | 0.3              |\n| Ritel         | 0.02             |\n| Pengemasan    | 0.07             |\n| Kerugian      | 0.18             |\n| Penggunaan Lahan | -0.03           |\n\n**Fakta Singkat tentang Keberlanjutan:** Pisang adalah buah tropis yang tumbuh di iklim hangat.  Meskipun pisang memiliki jejak karbon yang relatif rendah,  kita bisa mengurangi emisi lebih lanjut dengan memilih pisang lokal jika tersedia. \n\n**Saran:**\n\n🌱 **Beli pisang yang sudah matang:**  Ini membantu mengurangi pemborosan makanan dan emisi yang terkait dengan produksi pisang yang tidak terjual.\n\n🌍 **Pilih pisang organik:**  Memilih pisang organik mendukung praktik pertanian berkelanjutan yang lebih ramah lingkungan.\n\n♻️ **Gunakan kembali atau daur ulang kemasan pisang:**  Kemasan pisang seringkali terbuat dari bahan yang dapat didaur ulang, jadi pastikan untuk mengolahnya dengan baik.\n\n\"Setiap pilihan kecil yang kita buat, seperti memilih pisang lokal dan organik, berkontribusi pada masa depan yang lebih berkelanjutan.\" 🌎 \n\n\n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "nuts",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Analisis Emisi Karbon Kacang-kacangan 🥜\n\n**Ringkasan:** Kacang-kacangan adalah camilan yang lezat dan bergizi, yang merupakan sumber protein, lemak sehat, dan serat yang baik.\n\n**Jenis:** Vegetarian (Veg)\n\n**Total Emisi Karbon:** 3.26 kg CO2e\n\n**Rincian Emisi:**\n\n| Kategori      | Emisi (kg CO2e) |\n|--------------|-------------------|\n| Pertanian     | 3.37             |\n| Pengolahan   | 0.05             |\n| Transportasi  | 0.11             |\n| Ritel         | 0.04             |\n| Pengemasan    | 0.12             |\n| Kerugian      | -0.01            |\n| Penggunaan Lahan | -3.26           |\n\n**Fakta Singkat tentang Keberlanjutan:** Kacang-kacangan memiliki jejak karbon yang relatif rendah dibandingkan dengan produk hewani dan beberapa sumber protein lainnya.\n\n**Saran:**\n\n🌱 **Pilih kacang lokal:** Memilih kacang lokal dapat membantu mengurangi emisi transportasi dan mendukung petani lokal.\n\n🌍 **Pilih kacang organik:** Memilih kacang organik mendukung praktik pertanian yang lebih ramah lingkungan.\n\n🍃 **Simpan kacang dengan benar:** Simpan kacang dalam wadah kedap udara di tempat yang sejuk dan gelap untuk membantu memperpanjang masa simpan dan mengurangi pemborosan.\n\n♻️ **Daur ulang kemasan kacang:**  Pastikan untuk mendaur ulang kemasan kacang untuk mengurangi limbah.\n\n\"Kacang-kacangan adalah camilan yang lezat dan bergizi yang baik untuk tubuh dan bumi.  Dengan memilih kacang lokal, organik, dan dengan mengurangi pemborosan, kita dapat bersama-sama menjaga kesehatan planet kita.\" 🥜🌎 \n\n\n",
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
logo = Image.open("image/logo.png")

# Set Streamlit page configuration
st.set_page_config(
    page_title="Text Generative",
    page_icon=logo,
)

st.write("# Text Generative Page")

st.markdown(
    """
   In this project, we have developed a **Text Generative System** that can provide automatic answers based on image classification results. It's pretty straightforward: first, the uploaded image is processed using machine learning models to recognize or classify the objects or context in it.

Once the image is classified, the system will call the Gemini API to create appropriate and relevant answers. We integrate this API so that it can produce text that matches the classification results and the parameters we've set. So, the classification results are the basis for the system to create answers that match the needs or scenarios that are being run.
    """
)

# Create two columns: left (upload) and right (input text)
col1, col2 = st.columns(2)

# Left column: Upload Image
with col1:
    st.header("Upload Image")
    uploaded_file = st.file_uploader(
        "Upload an image of your food order", type=["jpg", "jpeg", "png"]
    )
    if st.button("Calculate", key="calculate_button"):
        if uploaded_file is not None:
            # Save the uploaded image
            with open("uploaded_image.png", "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Call the function to analyze the image (define this function yourself)
            result = analyze_image("uploaded_image.png")
            # Display the uploaded image and analysis result
            st.image("uploaded_image.png",
                     caption='Uploaded Food Order', use_column_width=True)
            st.write(result)
        else:
            st.error("Please upload an image to proceed.")

# Right column: Input Food Order
with col2:
    st.header("Enter Food Order")
    user_input = st.text_area("Enter your food order:", "")
    if st.button("Analyze", key="analyze_button"):
        if user_input:
            try:
                # Call the chat session and send the message
                response = chat_session.send_message(user_input)
                # Debug: Display raw response from chat session
                st.write(response.text)
            except InternalServerError as e:
                st.error(f"Internal server error: {e.message}")
        else:
            st.error("Please enter a food order.")
