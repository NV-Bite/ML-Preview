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
    system_instruction="""**Anda adalah asisten cerdas berbahasa indoenssia yang bertugas menganalisis dari gambarr makanan atau struck makanan dan menghitung jejak karbondari makanan tersebut.
  **\n\n**Instruksi:**
  \n\n1. **Identifikasi Item Makanan**:
  \n   - Tentukan apakah setiap item makanan bersifat vegetarian atau non-vegetarian.
  \n  - Buatlah daftar setiap item makanan beserta klasifikasinya (veg/non-veg).\n\n2. 
  Rincian Emisi Karbon:\n\n 
  - Menghitung emisi karbon berdasarkan data yang diberikan untuk pertanian, pengolahan, transportasi, ritel, pengemasan, kerugian, dan penggunaan lahan.
  \nCatatan Penting: Setiap makanan menghasilkan emisi yang berbeda. Faktor seperti jenis makanan (vegetarian atau non-vegetarian) mempengaruhi emisi secara signifikan.
  \n\n3. **Berikan Rincian**:
  \n   - Rincikan emisi karbon untuk setiap item makanan secara terpisah jika terdapat banyak jenis makanan.
  \n   - Buatlah ringkasan total emisi karbon makanan
  \n\n4. **Ringkaskan Hasil dengan Singkat**:
  \n   - Sertakan ringkasan singkat tentang makanan.
  \n   - Sebutkan jenis (veg/non-veg).
  \n   - Nyatakan total emisi karbon dalam tabel.
  \n   - Berikan rincian emisi yang relevan dengan kategori yang di sajikan seblumnya dan berikan saran yang bisa user terapkan untuk sustainability.
  \n\n5. berikan kata kata yang membuat user agar melakukan sustainability
  \n   - Contohnya : Jejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan.
  \n\nreferensi data yang boleh kamu akses dibawah ini:
  \n['Apples menghasilkan emisi 0.225815762 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.003820138 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.095804473 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016577621 kg CO2e dan 0.044526409 kg CO2e. Namun, terdapat kerugian sebesar 0.070807865 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.028951464 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.
  '\n 'Bananas menghasilkan emisi 0.269618358 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.06014592 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.295830362 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.020980708 kg CO2e dan 0.065670278 kg CO2e. Namun, terdapat kerugian sebesar 0.175184627 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.025533871 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.
  '\n 'Barley menghasilkan emisi 0.176376721 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.127702596 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.035351164 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.26358711 kg CO2e dan 0.496786387 kg CO2e. Namun, terdapat kerugian sebesar 0.070691954 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.00867555 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.
  '\n 'Beef (beef herd) menghasilkan emisi 56.22806279 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 1.811083009 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.494124578 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.233537838 kg CO2e dan 0.352084451 kg CO2e. Namun, terdapat kerugian sebesar 14.43999758 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 23.23753584 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.
  '\n 'Beef (dairy herd) menghasilkan emisi 21.91552941 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 1.547664428 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.592409815 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.254032327 kg CO2e dan 0.374549103 kg CO2e. Namun, terdapat kerugian sebesar 3.847514644 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 1.266022291 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Beet Sugar menghasilkan emisi 0.535721306 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.241885457 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.628543902 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.090289045 kg CO2e. Namun, terdapat kerugian sebesar 0.276262526 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 5.19e-05 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Berries & Grapes menghasilkan emisi 0.71784815 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.236391771 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.017056878 kg CO2e dan 0.211092325 kg CO2e. Namun, terdapat kerugian sebesar 0.324895121 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.024600997 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Brassicas menghasilkan emisi 0.277745354 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.094640882 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016843897 kg CO2e dan 0.045303061 kg CO2e. Namun, terdapat kerugian sebesar 0.077780876 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.002242361 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Cane Sugar menghasilkan emisi 0.491269852 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.037380973 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.794510292 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.036723005 kg CO2e dan 0.084277185 kg CO2e. Namun, terdapat kerugian sebesar 0.491722295 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 1.263040556 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Cassava menghasilkan emisi 0.219993617 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093597398 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.044821982 kg CO2e. Namun, terdapat kerugian sebesar 0.328503936 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.589435664 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Cheese menghasilkan emisi 13.0955392 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.740386293 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.138556663 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.333337741 kg CO2e dan 0.172090931 kg CO2e. Namun, terdapat kerugian sebesar 2.577136521 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 4.467476309 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Citrus Fruit menghasilkan emisi 0.306732538 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093855317 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016685298 kg CO2e dan 0.044735127 kg CO2e. Namun, terdapat kerugian sebesar 0.071570082 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.145953655 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Coffee menghasilkan emisi 10.75444008 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.613185194 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.134528124 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.052486794 kg CO2e dan 1.687496266 kg CO2e. Namun, terdapat kerugian sebesar 11.46697109 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 3.818798535 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Dark Chocolate menghasilkan emisi 6.68700226 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.333743892 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.110871398 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.037652218 kg CO2e dan 0.722433613 kg CO2e. Namun, terdapat kerugian sebesar 12.94020883 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 25.81483298 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Eggs menghasilkan emisi 1.319636556 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.084063931 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.035615941 kg CO2e dan 0.16143735 kg CO2e. Namun, terdapat kerugian sebesar 0.153323463 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.710381288 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Fish (farmed) menghasilkan emisi 8.056114834 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.044598632 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.247958628 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.089975618 kg CO2e dan 0.137537392 kg CO2e. Namun, terdapat kerugian sebesar 2.02712264 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 1.194717129 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Groundnuts menghasilkan emisi 1.575954219 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.410917506 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.132597229 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.046872605 kg CO2e dan 0.109439863 kg CO2e. Namun, terdapat kerugian sebesar 0.469079765 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.4851524 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Lamb & Mutton menghasilkan emisi 27.02574947 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 1.539596149 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.678854295 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.300814068 kg CO2e dan 0.34760362 kg CO2e. Namun, terdapat kerugian sebesar 5.898234517 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.648246975 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Maize menghasilkan emisi 0.717274411 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.078319173 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.090377117 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039312998 kg CO2e dan 0.09026754 kg CO2e. Namun, terdapat kerugian sebesar 0.210791222 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.475169036 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Milk menghasilkan emisi 1.508862035 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.154189035 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093235401 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.265149784 kg CO2e dan 0.100180454 kg CO2e. Namun, terdapat kerugian sebesar 0.274066289 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.51222255 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Nuts menghasilkan emisi 3.374406815 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.051419528 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.106734489 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.042638569 kg CO2e dan 0.123747546 kg CO2e. Namun, terdapat kerugian sebesar -0.007999532 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -3.257812133 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Oatmeal menghasilkan emisi 1.872373655 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.057838235 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.091276148 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.090289045 kg CO2e. Namun, terdapat kerugian sebesar 0.327418343 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.001931697 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Olive Oil menghasilkan emisi 3.672172059 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.567188828 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.414114186 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.740116693 kg CO2e. Namun, terdapat kerugian sebesar 0.315646031 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.323684317 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Onions & Leeks menghasilkan emisi 0.211039002 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.094781878 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039249706 kg CO2e dan 0.044784978 kg CO2e. Namun, terdapat kerugian sebesar 0.102098528 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.004808972 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Other Fruit menghasilkan emisi 0.372578972 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.015557815 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.183164953 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016432178 kg CO2e dan 0.041961205 kg CO2e. Namun, terdapat kerugian sebesar 0.296021624 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.127035306 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Other Pulses menghasilkan emisi 1.08871478 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.09617697 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.353229974 kg CO2e. Namun, terdapat kerugian sebesar 0.17563304 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.033302446 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Other Vegetables menghasilkan emisi 0.176173078 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.060405149 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.165549737 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.015135273 kg CO2e dan 0.041747507 kg CO2e. Namun, terdapat kerugian sebesar 0.071981328 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.001180576 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Palm Oil menghasilkan emisi 1.875131956 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 1.125325738 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.185116868 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.038737674 kg CO2e dan 0.788108048 kg CO2e. Namun, terdapat kerugian sebesar 0.548765131 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 2.755585078 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Peas menghasilkan emisi 0.717159966 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.095067089 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.044821982 kg CO2e. Namun, terdapat kerugian sebesar 0.078590739 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.000118777 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Pig Meat menghasilkan emisi 2.477097669 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.415841843 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.501263865 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.278096013 kg CO2e dan 0.432286318 kg CO2e. Namun, terdapat kerugian sebesar 1.658551095 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 2.244068682 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Potatoes menghasilkan emisi 0.193083415 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093867162 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039243544 kg CO2e dan 0.044549374 kg CO2e. Namun, terdapat kerugian sebesar 0.090705705 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.001315101 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Poultry Meat menghasilkan emisi 0.927821834 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.607372729 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.381078302 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.243976607 kg CO2e dan 0.292702383 kg CO2e. Namun, terdapat kerugian sebesar 1.452085944 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 3.508428798 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Rapeseed Oil menghasilkan emisi 2.156630103 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.177875305 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.17514717 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.042540886 kg CO2e dan 0.776637791 kg CO2e. Namun, terdapat kerugian sebesar 0.243266575 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.195574761 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Rice menghasilkan emisi 3.553953627 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.065220036 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.095619114 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.063362152 kg CO2e dan 0.083853899 kg CO2e. Namun, terdapat kerugian sebesar 0.611516643 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.02187964 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Root Vegetables menghasilkan emisi 0.153994029 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.113769657 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.038855213 kg CO2e dan 0.044662141 kg CO2e. Namun, terdapat kerugian sebesar 0.061609681 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.013389332 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Shrimps (farmed) menghasilkan emisi 13.45397854 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.330851591 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.352361124 kg CO2e dan 0.536147297 kg CO2e. Namun, terdapat kerugian sebesar 7.832022151 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.330563074 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Soy milk menghasilkan emisi 0.092768045 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.162509105 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.109835191 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.27017249 kg CO2e dan 0.098395215 kg CO2e. Namun, terdapat kerugian sebesar 0.061527272 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.179971835 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Soybean Oil menghasilkan emisi 1.406293945 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.287775815 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.276950302 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039402755 kg CO2e dan 0.786068449 kg CO2e. Namun, terdapat kerugian sebesar 0.661796404 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 2.866183849 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Sunflower Oil menghasilkan emisi 1.976377998 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.210714429 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.18454226 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.784464695 kg CO2e. Namun, terdapat kerugian sebesar 0.28163571 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.122421009 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Tofu menghasilkan emisi 0.494701474 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.793884503 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.176925292 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.27017249 kg CO2e dan 0.177360572 kg CO2e. Namun, terdapat kerugian sebesar 0.290470423 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.958229607 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Tomatoes menghasilkan emisi 0.705446792 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.012381556 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.177110774 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016691531 kg CO2e dan 0.145671363 kg CO2e. Namun, terdapat kerugian sebesar 0.658417374 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.372987265 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Wheat & Rye menghasilkan emisi 0.820300153 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.210128771 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.125440977 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.05604907 kg CO2e dan 0.086838974 kg CO2e. Namun, terdapat kerugian sebesar 0.17793509 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.097130028 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'\n 'Wine menghasilkan emisi 0.626026936 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.138626407 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093284143 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.749231524 kg CO2e. Namun, terdapat kerugian sebesar 0.203535757 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.061264312 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.']\n""",
)


chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "apple",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari apel:\n\n**Ringkasan Makanan:**\n- Apel\n- Vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 0.225815762 |\n| Pengolahan      | 0.003820138 |\n| Transportasi     | 0.095804473 |\n| Ritel           | 0.016577621 |\n| Pengemasan      | 0.044526409 |\n| Kerugian         | 0.070807865 |\n| Penggunaan Lahan | -0.028951464 |\n| **Total**       | **0.337570744** |\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan.\n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "banana",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari pisang:\n\n**Ringkasan Makanan:**\n- Pisang\n- Vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 0.269618358 |\n| Pengolahan      | 0.06014592  |\n| Transportasi     | 0.295830362 |\n| Ritel           | 0.020980708 |\n| Pengemasan      | 0.065670278 |\n| Kerugian         | 0.175184627 |\n| Penggunaan Lahan | -0.025533871 |\n| **Total**       | **0.806765174** |\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "rice",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari nasi:\n\n**Ringkasan Makanan:**\n- Nasi\n- Vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 3.553953627 |\n| Pengolahan      | 0.065220036 |\n| Transportasi     | 0.095619114 |\n| Ritel           | 0.063362152 |\n| Pengemasan      | 0.083853899 |\n| Kerugian         | 0.611516643 |\n| Penggunaan Lahan | -0.02187964  |\n| **Total**       | **4.342735735** |\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan.\n\nPerhatikan bahwa nasi memiliki jejak karbon yang relatif tinggi, terutama karena proses pertaniannya yang intensif. Sebagai alternatif, Anda dapat mempertimbangkan untuk mengkonsumsi nasi merah atau nasi merah yang merupakan pilihan yang lebih berkelanjutan.  \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "cheese",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari keju:\n\n**Ringkasan Makanan:**\n- Keju\n- Non-vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 13.0955392  |\n| Pengolahan      | 0.740386293 |\n| Transportasi     | 0.138556663 |\n| Ritel           | 0.333337741 |\n| Pengemasan      | 0.172090931 |\n| Kerugian         | 2.577136521 |\n| Penggunaan Lahan | 4.467476309 |\n| **Total**       | **21.524527667** |\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan.\n\nPerhatikan bahwa keju memiliki jejak karbon yang relatif tinggi, terutama karena proses pertanian dan pengolahannya yang intensif. Sebagai alternatif, Anda dapat mempertimbangkan untuk mengkonsumsi keju dengan lebih sedikit lemak atau keju yang terbuat dari susu organik, yang dapat memiliki jejak karbon yang lebih rendah. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "apple",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari apel:\n\n**Ringkasan Makanan:**\n- Apel\n- Vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 0.225815762 |\n| Pengolahan      | 0.003820138 |\n| Transportasi     | 0.095804473 |\n| Ritel           | 0.016577621 |\n| Pengemasan      | 0.044526409 |\n| Kerugian         | 0.070807865 |\n| Penggunaan Lahan | -0.028951464 |\n| **Total**       | **0.337570744** |\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan.\n\n**Saran untuk Berkelanjutan:**\n\n- **Belilah apel lokal:** Memilih apel lokal mengurangi emisi transportasi.\n- **Belilah apel organik:** Pertanian organik biasanya memiliki dampak lingkungan yang lebih rendah.\n- **Belilah apel dalam jumlah yang dibutuhkan:** Mengurangi pemborosan makanan dapat membantu mengurangi emisi karbon keseluruhan. \n\nAnda juga dapat mencoba menanam apel sendiri! 🍎  \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "cheese",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari keju:\n\n**Ringkasan Makanan:**\n- Keju\n- Non-vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 13.0955392  |\n| Pengolahan      | 0.740386293 |\n| Transportasi     | 0.138556663 |\n| Ritel           | 0.333337741 |\n| Pengemasan      | 0.172090931 |\n| Kerugian         | 2.577136521 |\n| Penggunaan Lahan | 4.467476309 |\n| **Total**       | **21.524527667** |\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan.\n\n**Saran untuk Sustainability:**\n\n- **Pilih Keju Lokal:**  Memilih keju yang diproduksi lokal mengurangi emisi transportasi.\n- **Pilih Keju Organik:**  Keju organik biasanya berasal dari sapi yang diberi makan rumput dan dipelihara dalam sistem yang lebih ramah lingkungan.\n- **Pilih Keju dengan Lemak Rendah:**  Keju dengan lemak rendah umumnya memiliki jejak karbon yang lebih rendah.\n\nMembuat perubahan kecil dalam kebiasaan makan Anda dapat membantu mengurangi jejak karbon Anda dan menciptakan masa depan yang lebih berkelanjutan. \n\n\n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "nasi goreng",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Sulit untuk menghitung jejak karbon nasi goreng secara pasti karena tergantung pada banyak faktor seperti:\n\n* **Jenis nasi:** Nasi putih, nasi merah, nasi hitam, dll. masing-masing memiliki jejak karbon yang berbeda.\n* **Bahan-bahan:** Nasi goreng biasanya mengandung berbagai bahan seperti telur, ayam, sayuran, minyak, dan bumbu-bumbu. Setiap bahan memiliki jejak karbon yang berbeda.\n* **Metode memasak:** Memasak nasi goreng di atas kompor gas, kompor listrik, atau menggunakan wajan dengan lapisan anti lengket akan menghasilkan jejak karbon yang berbeda.\n* **Sumber bahan:** Bahan-bahan yang berasal dari lokal akan memiliki jejak karbon yang lebih rendah dibandingkan bahan-bahan yang diimpor.\n\nNamun, kita dapat memberikan estimasi kasar dengan mempertimbangkan bahwa nasi goreng terdiri dari nasi dan beberapa bahan tambahan:\n\n**Asumsi:**\n\n* Nasi goreng terdiri dari 100 gram nasi dan 50 gram bahan tambahan (telur, ayam, sayuran, minyak, bumbu).\n* Jejak karbon nasi putih adalah sekitar 3.5 kg CO2e per kg.\n* Jejak karbon rata-rata bahan tambahan adalah 2 kg CO2e per kg (ini adalah estimasi kasar, jejak karbon sebenarnya bisa lebih tinggi atau lebih rendah tergantung pada bahan-bahan yang digunakan).\n\n**Perhitungan:**\n\n* Jejak karbon nasi: 0.1 kg (100 gram) * 3.5 kg CO2e/kg = 0.35 kg CO2e\n* Jejak karbon bahan tambahan: 0.05 kg * 2 kg CO2e/kg = 0.1 kg CO2e\n* **Jejak karbon total nasi goreng: 0.35 kg CO2e + 0.1 kg CO2e = 0.45 kg CO2e**\n\n**Saran untuk Sustainability:**\n\n* **Pilih nasi merah atau nasi hitam:**  Nasi merah dan nasi hitam memiliki jejak karbon yang lebih rendah daripada nasi putih.\n* **Pilih bahan-bahan lokal:**  Memilih bahan-bahan yang diproduksi lokal mengurangi emisi transportasi.\n* **Kurangi penggunaan minyak:**  Memasak dengan sedikit minyak dapat mengurangi emisi karbon.\n* **Dukung penggunaan energi terbarukan:**  Pilih restoran yang menggunakan sumber energi terbarukan untuk memasak.\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. \n\nIngatlah bahwa perhitungan ini hanya estimasi kasar. Jejak karbon sebenarnya dari nasi goreng dapat bervariasi tergantung pada faktor-faktor yang disebutkan di atas. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "apple",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari apel:\n\n**Ringkasan Makanan:**\n- Apel\n- Vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 0.225815762 |\n| Pengolahan      | 0.003820138 |\n| Transportasi     | 0.095804473 |\n| Ritel           | 0.016577621 |\n| Pengemasan      | 0.044526409 |\n| Kerugian         | 0.070807865 |\n| Penggunaan Lahan | -0.028951464 |\n| **Total**       | **0.337570744** |\n\n**Saran untuk Sustainability:**\n\n- **Belilah apel lokal:** Memilih apel lokal mengurangi emisi transportasi.\n- **Belilah apel organik:** Pertanian organik biasanya memiliki dampak lingkungan yang lebih rendah.\n- **Belilah apel dalam jumlah yang dibutuhkan:** Mengurangi pemborosan makanan dapat membantu mengurangi emisi karbon keseluruhan. \n- **Pertimbangkan untuk menanam apel sendiri!** 🍎 \n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. \n\nSemoga informasi ini bermanfaat! \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "banana",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari pisang:\n\n**Ringkasan Makanan:**\n- Pisang\n- Vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 0.269618358 |\n| Pengolahan      | 0.06014592  |\n| Transportasi     | 0.295830362 |\n| Ritel           | 0.020980708 |\n| Pengemasan      | 0.065670278 |\n| Kerugian         | 0.175184627 |\n| Penggunaan Lahan | -0.025533871 |\n| **Total**       | **0.806765174** |\n\n**Saran untuk Sustainability:**\n\n- **Belilah pisang lokal:** Memilih pisang lokal mengurangi emisi transportasi.\n- **Belilah pisang organik:** Pertanian organik biasanya memiliki dampak lingkungan yang lebih rendah.\n- **Belilah pisang dalam jumlah yang dibutuhkan:** Mengurangi pemborosan makanan dapat membantu mengurangi emisi karbon keseluruhan. \n- **Pertimbangkan untuk menanam pisang sendiri!** 🍌 (Jika Anda tinggal di daerah beriklim tropis)\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. \n\nSemoga informasi ini bermanfaat! \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "rice",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Berikut adalah rincian jejak karbon dari nasi:\n\n**Ringkasan Makanan:**\n- Nasi\n- Vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 3.553953627 |\n| Pengolahan      | 0.065220036 |\n| Transportasi     | 0.095619114 |\n| Ritel           | 0.063362152 |\n| Pengemasan      | 0.083853899 |\n| Kerugian         | 0.611516643 |\n| Penggunaan Lahan | -0.02187964  |\n| **Total**       | **4.342735735** |\n\n**Saran untuk Sustainability:**\n\n* **Pilih nasi merah atau nasi hitam:**  Nasi merah dan nasi hitam memiliki jejak karbon yang lebih rendah daripada nasi putih.\n* **Belilah nasi lokal:**  Memilih nasi yang diproduksi lokal mengurangi emisi transportasi.\n* **Kurangi pemborosan makanan:**  Memasak nasi dalam jumlah yang tepat dan menyimpan sisa nasi dengan benar dapat mengurangi pemborosan.\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. \n\nSemoga informasi ini bermanfaat! \n\n\n",
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
                "Berikut adalah rincian jejak karbon dari daging sapi:\n\n**Ringkasan Makanan:**\n- Daging sapi\n- Non-vegetarian\n\n**Emisi Karbon (kg CO2e):**\n\n| Kategori        | Emisi       |\n|-----------------|--------------|\n| Pertanian       | 56.22806279 |\n| Pengolahan      | 1.811083009 |\n| Transportasi     | 0.494124578 |\n| Ritel           | 0.233537838 |\n| Pengemasan      | 0.352084451 |\n| Kerugian         | 14.43999758 |\n| Penggunaan Lahan | 23.23753584 |\n| **Total**       | **96.796442084** |\n\n**Saran untuk Sustainability:**\n\n* **Pilih daging sapi organik:**  Sapi organik dipelihara dalam sistem yang lebih ramah lingkungan dan biasanya memiliki jejak karbon yang lebih rendah.\n* **Pilih daging sapi lokal:**  Memilih daging sapi yang diproduksi lokal mengurangi emisi transportasi.\n\nJejak karbon dari konsumsi makanan adalah kontributor signifikan terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. \n\nSebagai catatan, jejak karbon daging sapi dapat bervariasi tergantung pada metode pemeliharaan, pakan, dan jarak transportasi.  \n\n\n",
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
