import streamlit as st
import google.generativeai as genai
from PIL import Image
from pathlib import Path
from google.api_core.exceptions import InternalServerError
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("API_KEY")

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
    **Anda adalah asisten cerdas yang bertugas menghitung jejak karbon pada makanan.**

instruksi 
1. **Identifikasi Item Makanan:**
   - Tentukan setiap item makanan yang dikonsumsi, dan klasifikasikan apakah makanan tersebut termasuk vegetarian atau non-vegetarian.
   - Buat daftar makanan beserta kategorinya (vegetarian atau non-vegetarian) untuk mempermudah perhitungan emisi karbon.

2. **Perhitungan Emisi Karbon:**
   - Hitung emisi karbon dari setiap makanan berdasarkan aspek-aspek berikut: 
      - **Pertanian**: Emisi yang dihasilkan dari proses penanaman atau peternakan.
      - **Pengolahan**: Emisi dari proses pengolahan bahan baku menjadi produk akhir.
      - **Transportasi**: Emisi dari pengangkutan makanan hingga ke titik distribusi.
      - **Ritel**: Emisi dari penjualan, termasuk penyimpanan di toko.
      - **Pengemasan**: Emisi dari penggunaan bahan kemasan.
      - **Kerugian**: Emisi dari makanan yang terbuang atau tidak terpakai.
      - **Penggunaan Lahan**: Emisi dari dampak pemanfaatan lahan.
   - Perhatikan bahwa jenis makanan (vegetarian atau non-vegetarian) memiliki dampak yang berbeda terhadap emisi karbon. Umumnya, makanan non-vegetarian cenderung memiliki emisi lebih tinggi dibandingkan dengan makanan vegetarian.

3. **Rincian Emisi Karbon:**
   - Rincikan emisi karbon untuk setiap item makanan secara terpisah, terutama jika terdapat berbagai jenis makanan dalam daftar. Sertakan angka yang relevan untuk memperjelas kontribusi emisi dari setiap kategori di atas.
   - Berikan total emisi karbon dari seluruh makanan yang dikonsumsi agar user dapat melihat dampak keseluruhannya.

4. **Ringkasan Hasil dan Saran Praktik Berkelanjutan:**
   - Setelah menghitung total emisi karbon beriukan saran dengan format seperti ini:
      - **Belilah makanan secukupnya:** Mengurangi pemborosan makanan turut membantu menurunkan emisi karbon secara signifikan.
      - **Pilih produk lokal:** Mengonsumsi makanan yang diproduksi secara lokal dapat mengurangi emisi karbon dari transportasi jarak jauh.
      - **Pilih makanan organik:** Produk organik biasanya dihasilkan melalui praktik berkelanjutan yang lebih ramah lingkungan.
      - **Gunakan kemasan ramah lingkungan:** Pilih makanan yang dikemas dengan bahan yang dapat didaur ulang atau diurai oleh alam (kompos).

5. **Ajakan untuk Berkelanjutan:**
   - "Jejak karbon dari konsumsi makanan adalah salah satu kontributor besar terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. Mari kita berkontribusi dalam menjaga bumi ini dengan memilih makanan yang mendukung keberlanjutan dan mengurangi jejak karbon dari konsumsi kita sehari-hari."

referensi data yang boleh kamu akses dibawah ini:
['Apples menghasilkan emisi 0.225815762 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.003820138 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.095804473 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016577621 kg CO2e dan 0.044526409 kg CO2e. Namun, terdapat kerugian sebesar 0.070807865 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.028951464 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Bananas menghasilkan emisi 0.269618358 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.06014592 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.295830362 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.020980708 kg CO2e dan 0.065670278 kg CO2e. Namun, terdapat kerugian sebesar 0.175184627 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.025533871 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Barley menghasilkan emisi 0.176376721 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.127702596 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.035351164 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.26358711 kg CO2e dan 0.496786387 kg CO2e. Namun, terdapat kerugian sebesar 0.070691954 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.00867555 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Beef (beef herd) menghasilkan emisi 56.22806279 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 1.811083009 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.494124578 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.233537838 kg CO2e dan 0.352084451 kg CO2e. Namun, terdapat kerugian sebesar 14.43999758 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 23.23753584 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Beef (dairy herd) menghasilkan emisi 21.91552941 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 1.547664428 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.592409815 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.254032327 kg CO2e dan 0.374549103 kg CO2e. Namun, terdapat kerugian sebesar 3.847514644 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 1.266022291 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Beet Sugar menghasilkan emisi 0.535721306 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.241885457 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.628543902 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.090289045 kg CO2e. Namun, terdapat kerugian sebesar 0.276262526 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 5.19e-05 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Berries & Grapes menghasilkan emisi 0.71784815 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.236391771 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.017056878 kg CO2e dan 0.211092325 kg CO2e. Namun, terdapat kerugian sebesar 0.324895121 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.024600997 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Brassicas menghasilkan emisi 0.277745354 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.094640882 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016843897 kg CO2e dan 0.045303061 kg CO2e. Namun, terdapat kerugian sebesar 0.077780876 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.002242361 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Cane Sugar menghasilkan emisi 0.491269852 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.037380973 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.794510292 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.036723005 kg CO2e dan 0.084277185 kg CO2e. Namun, terdapat kerugian sebesar 0.491722295 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 1.263040556 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Cassava menghasilkan emisi 0.219993617 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093597398 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.044821982 kg CO2e. Namun, terdapat kerugian sebesar 0.328503936 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.589435664 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Cheese menghasilkan emisi 13.0955392 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.740386293 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.138556663 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.333337741 kg CO2e dan 0.172090931 kg CO2e. Namun, terdapat kerugian sebesar 2.577136521 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 4.467476309 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Citrus Fruit menghasilkan emisi 0.306732538 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093855317 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016685298 kg CO2e dan 0.044735127 kg CO2e. Namun, terdapat kerugian sebesar 0.071570082 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.145953655 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Coffee menghasilkan emisi 10.75444008 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.613185194 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.134528124 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.052486794 kg CO2e dan 1.687496266 kg CO2e. Namun, terdapat kerugian sebesar 11.46697109 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 3.818798535 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Dark Chocolate menghasilkan emisi 6.68700226 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.333743892 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.110871398 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.037652218 kg CO2e dan 0.722433613 kg CO2e. Namun, terdapat kerugian sebesar 12.94020883 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 25.81483298 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Eggs menghasilkan emisi 1.319636556 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.084063931 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.035615941 kg CO2e dan 0.16143735 kg CO2e. Namun, terdapat kerugian sebesar 0.153323463 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.710381288 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Fish (farmed) menghasilkan emisi 8.056114834 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.044598632 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.247958628 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.089975618 kg CO2e dan 0.137537392 kg CO2e. Namun, terdapat kerugian sebesar 2.02712264 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 1.194717129 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Groundnuts menghasilkan emisi 1.575954219 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.410917506 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.132597229 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.046872605 kg CO2e dan 0.109439863 kg CO2e. Namun, terdapat kerugian sebesar 0.469079765 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.4851524 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Lamb & Mutton menghasilkan emisi 27.02574947 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 1.539596149 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.678854295 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.300814068 kg CO2e dan 0.34760362 kg CO2e. Namun, terdapat kerugian sebesar 5.898234517 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.648246975 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Maize menghasilkan emisi 0.717274411 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.078319173 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.090377117 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039312998 kg CO2e dan 0.09026754 kg CO2e. Namun, terdapat kerugian sebesar 0.210791222 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.475169036 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Milk menghasilkan emisi 1.508862035 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.154189035 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093235401 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.265149784 kg CO2e dan 0.100180454 kg CO2e. Namun, terdapat kerugian sebesar 0.274066289 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.51222255 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Nuts menghasilkan emisi 3.374406815 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.051419528 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.106734489 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.042638569 kg CO2e dan 0.123747546 kg CO2e. Namun, terdapat kerugian sebesar -0.007999532 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -3.257812133 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Oatmeal menghasilkan emisi 1.872373655 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.057838235 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.091276148 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.090289045 kg CO2e. Namun, terdapat kerugian sebesar 0.327418343 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.001931697 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Olive Oil menghasilkan emisi 3.672172059 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.567188828 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.414114186 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.740116693 kg CO2e. Namun, terdapat kerugian sebesar 0.315646031 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.323684317 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Onions & Leeks menghasilkan emisi 0.211039002 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.094781878 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039249706 kg CO2e dan 0.044784978 kg CO2e. Namun, terdapat kerugian sebesar 0.102098528 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.004808972 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Other Fruit menghasilkan emisi 0.372578972 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.015557815 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.183164953 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016432178 kg CO2e dan 0.041961205 kg CO2e. Namun, terdapat kerugian sebesar 0.296021624 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.127035306 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Other Pulses menghasilkan emisi 1.08871478 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.09617697 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.353229974 kg CO2e. Namun, terdapat kerugian sebesar 0.17563304 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.033302446 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Other Vegetables menghasilkan emisi 0.176173078 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.060405149 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.165549737 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.015135273 kg CO2e dan 0.041747507 kg CO2e. Namun, terdapat kerugian sebesar 0.071981328 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.001180576 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Palm Oil menghasilkan emisi 1.875131956 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 1.125325738 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.185116868 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.038737674 kg CO2e dan 0.788108048 kg CO2e. Namun, terdapat kerugian sebesar 0.548765131 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 2.755585078 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Peas menghasilkan emisi 0.717159966 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.095067089 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.044821982 kg CO2e. Namun, terdapat kerugian sebesar 0.078590739 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.000118777 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Pig Meat menghasilkan emisi 2.477097669 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.415841843 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.501263865 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.278096013 kg CO2e dan 0.432286318 kg CO2e. Namun, terdapat kerugian sebesar 1.658551095 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 2.244068682 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Potatoes menghasilkan emisi 0.193083415 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093867162 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039243544 kg CO2e dan 0.044549374 kg CO2e. Namun, terdapat kerugian sebesar 0.090705705 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.001315101 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Poultry Meat menghasilkan emisi 0.927821834 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.607372729 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.381078302 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.243976607 kg CO2e dan 0.292702383 kg CO2e. Namun, terdapat kerugian sebesar 1.452085944 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 3.508428798 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Rapeseed Oil menghasilkan emisi 2.156630103 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.177875305 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.17514717 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.042540886 kg CO2e dan 0.776637791 kg CO2e. Namun, terdapat kerugian sebesar 0.243266575 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.195574761 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Rice menghasilkan emisi 3.553953627 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.065220036 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.095619114 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.063362152 kg CO2e dan 0.083853899 kg CO2e. Namun, terdapat kerugian sebesar 0.611516643 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.02187964 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Root Vegetables menghasilkan emisi 0.153994029 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.113769657 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.038855213 kg CO2e dan 0.044662141 kg CO2e. Namun, terdapat kerugian sebesar 0.061609681 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.013389332 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Shrimps (farmed) menghasilkan emisi 13.45397854 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.0 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.330851591 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.352361124 kg CO2e dan 0.536147297 kg CO2e. Namun, terdapat kerugian sebesar 7.832022151 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.330563074 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Soy milk menghasilkan emisi 0.092768045 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.162509105 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.109835191 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.27017249 kg CO2e dan 0.098395215 kg CO2e. Namun, terdapat kerugian sebesar 0.061527272 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.179971835 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Soybean Oil menghasilkan emisi 1.406293945 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.287775815 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.276950302 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039402755 kg CO2e dan 0.786068449 kg CO2e. Namun, terdapat kerugian sebesar 0.661796404 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 2.866183849 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Sunflower Oil menghasilkan emisi 1.976377998 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.210714429 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.18454226 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.784464695 kg CO2e. Namun, terdapat kerugian sebesar 0.28163571 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.122421009 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Tofu menghasilkan emisi 0.494701474 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.793884503 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.176925292 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.27017249 kg CO2e dan 0.177360572 kg CO2e. Namun, terdapat kerugian sebesar 0.290470423 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.958229607 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Tomatoes menghasilkan emisi 0.705446792 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.012381556 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.177110774 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.016691531 kg CO2e dan 0.145671363 kg CO2e. Namun, terdapat kerugian sebesar 0.658417374 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.372987265 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Wheat & Rye menghasilkan emisi 0.820300153 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.210128771 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.125440977 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.05604907 kg CO2e dan 0.086838974 kg CO2e. Namun, terdapat kerugian sebesar 0.17793509 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi 0.097130028 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.'
 'Wine menghasilkan emisi 0.626026936 kg CO2e dari pertanian. Selama proses pengolahan, emisi tambahan sebesar 0.138626407 kg CO2e dihasilkan. Transportasi produk ini menghasilkan 0.093284143 kg CO2e. Emisi dari sektor ritel dan pengemasan masing-masing adalah 0.039322364 kg CO2e dan 0.749231524 kg CO2e. Namun, terdapat kerugian sebesar 0.203535757 kg CO2e selama proses tersebut. Penggunaan lahan untuk produksi ini menghasilkan emisi -0.061264312 kg CO2e, yang menunjukkan dampak negatif terhadap lingkungan.']
 """,
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
                "Jejak karbon dari 1 buah apel adalah sekitar **0.456 kg CO2e**. \n\nRincian emisi:\n\n* **Pertanian:** 0.225815762 kg CO2e\n* **Pengolahan:** 0.003820138 kg CO2e\n* **Transportasi:** 0.095804473 kg CO2e\n* **Ritel:** 0.016577621 kg CO2e\n* **Pengemasan:** 0.044526409 kg CO2e\n* **Kerugian:** 0.070807865 kg CO2e\n* **Penggunaan Lahan:** -0.028951464 kg CO2e (dampak negatif terhadap lingkungan)\n\nSaran praktis:\n\n* **Belilah apel secukupnya:** Mengurangi pemborosan makanan turut membantu menurunkan emisi karbon secara signifikan.\n* **Pilih apel lokal:** Mengonsumsi makanan yang diproduksi secara lokal dapat mengurangi emisi karbon dari transportasi jarak jauh.\n* **Pilih apel organik:** Produk organik biasanya dihasilkan melalui praktik berkelanjutan yang lebih ramah lingkungan.\n* **Gunakan kemasan ramah lingkungan:** Pilih apel yang dikemas dengan bahan yang dapat didaur ulang atau diurai oleh alam (kompos).\n\nJejak karbon dari konsumsi makanan adalah salah satu kontributor besar terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. Mari kita berkontribusi dalam menjaga bumi ini dengan memilih makanan yang mendukung keberlanjutan dan mengurangi jejak karbon dari konsumsi kita sehari-hari.\n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "beef herd",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Jejak karbon dari 1 kg daging sapi (beef herd) adalah sekitar **79.5 kg CO2e**.\n\nRincian emisi:\n\n* **Pertanian:** 56.22806279 kg CO2e\n* **Pengolahan:** 1.811083009 kg CO2e\n* **Transportasi:** 0.494124578 kg CO2e\n* **Ritel:** 0.233537838 kg CO2e\n* **Pengemasan:** 0.352084451 kg CO2e\n* **Kerugian:** 14.43999758 kg CO2e\n* **Penggunaan Lahan:** 23.23753584 kg CO2e (dampak negatif terhadap lingkungan)\n\nSaran praktis:\n\n* **Kurangi konsumsi daging sapi:** Daging sapi memiliki jejak karbon yang sangat tinggi. Mengurangi konsumsi daging sapi dan menggantinya dengan alternatif protein yang lebih rendah emisinya, seperti kacang-kacangan, tahu, atau ayam, dapat secara signifikan mengurangi jejak karbon Anda.\n* **Pilih daging sapi lokal:** Mengonsumsi daging sapi yang diproduksi secara lokal dapat mengurangi emisi karbon dari transportasi jarak jauh.\n* **Pilih daging sapi organik:** Produk organik biasanya dihasilkan melalui praktik berkelanjutan yang lebih ramah lingkungan.\n* **Kurangi pemborosan makanan:** Mengurangi pemborosan makanan, termasuk daging sapi, merupakan langkah penting dalam mengurangi emisi karbon.\n\nJejak karbon dari konsumsi makanan adalah salah satu kontributor besar terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. Mari kita berkontribusi dalam menjaga bumi ini dengan memilih makanan yang mendukung keberlanjutan dan mengurangi jejak karbon dari konsumsi kita sehari-hari. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "- beef heard ",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Jejak karbon dari 1 kg daging sapi (beef herd) adalah sekitar **79.5 kg CO2e**.\n\nRincian emisi:\n\n* **Pertanian:** 56.22806279 kg CO2e\n* **Pengolahan:** 1.811083009 kg CO2e\n* **Transportasi:** 0.494124578 kg CO2e\n* **Ritel:** 0.233537838 kg CO2e\n* **Pengemasan:** 0.352084451 kg CO2e\n* **Kerugian:** 14.43999758 kg CO2e\n* **Penggunaan Lahan:** 23.23753584 kg CO2e (dampak negatif terhadap lingkungan)\n\nSaran praktis:\n\n* **Kurangi konsumsi daging sapi:** Daging sapi memiliki jejak karbon yang sangat tinggi. Mengurangi konsumsi daging sapi dan menggantinya dengan alternatif protein yang lebih rendah emisinya, seperti kacang-kacangan, tahu, atau ayam, dapat secara signifikan mengurangi jejak karbon Anda.\n* **Pilih daging sapi lokal:** Mengonsumsi daging sapi yang diproduksi secara lokal dapat mengurangi emisi karbon dari transportasi jarak jauh.\n* **Pilih daging sapi organik:** Produk organik biasanya dihasilkan melalui praktik berkelanjutan yang lebih ramah lingkungan.\n* **Kurangi pemborosan makanan:** Mengurangi pemborosan makanan, termasuk daging sapi, merupakan langkah penting dalam mengurangi emisi karbon.\n\nJejak karbon dari konsumsi makanan adalah salah satu kontributor besar terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. Mari kita berkontribusi dalam menjaga bumi ini dengan memilih makanan yang mendukung keberlanjutan dan mengurangi jejak karbon dari konsumsi kita sehari-hari. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "beef heard\ncheese\nshrimps",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Jejak karbon dari makanan yang Anda sebutkan adalah:\n\n* **Beef (herd):** 79.5 kg CO2e per kg \n* **Cheese:** 13.0955392 kg CO2e per kg\n* **Shrimps (farmed):** 13.45397854 kg CO2e per kg\n\nTotal emisi karbon dari 1 kg beef, 1 kg cheese, dan 1 kg shrimps adalah **106.05 kg CO2e**. \n\n**Rincian emisi:**\n\n**Beef (herd)**\n\n* **Pertanian:** 56.22806279 kg CO2e\n* **Pengolahan:** 1.811083009 kg CO2e\n* **Transportasi:** 0.494124578 kg CO2e\n* **Ritel:** 0.233537838 kg CO2e\n* **Pengemasan:** 0.352084451 kg CO2e\n* **Kerugian:** 14.43999758 kg CO2e\n* **Penggunaan Lahan:** 23.23753584 kg CO2e (dampak negatif terhadap lingkungan)\n\n**Cheese:**\n\n* **Pertanian:** 13.0955392 kg CO2e\n* **Pengolahan:** 0.740386293 kg CO2e\n* **Transportasi:** 0.138556663 kg CO2e\n* **Ritel:** 0.333337741 kg CO2e\n* **Pengemasan:** 0.172090931 kg CO2e\n* **Kerugian:** 2.577136521 kg CO2e\n* **Penggunaan Lahan:** 4.467476309 kg CO2e (dampak negatif terhadap lingkungan)\n\n**Shrimps (farmed):**\n\n* **Pertanian:** 13.45397854 kg CO2e\n* **Pengolahan:** 0.0 kg CO2e\n* **Transportasi:** 0.330851591 kg CO2e\n* **Ritel:** 0.352361124 kg CO2e\n* **Pengemasan:** 0.536147297 kg CO2e\n* **Kerugian:** 7.832022151 kg CO2e\n* **Penggunaan Lahan:** 0.330563074 kg CO2e (dampak negatif terhadap lingkungan)\n\n**Saran Praktis:**\n\n* **Kurangi konsumsi daging:** Daging sapi dan udang memiliki jejak karbon yang sangat tinggi. Mengurangi konsumsi daging dan menggantinya dengan alternatif protein seperti kacang-kacangan, tahu, ayam, atau ikan yang ditangkap di laut dapat secara signifikan mengurangi jejak karbon Anda.\n* **Pilih produk lokal:** Mengonsumsi produk lokal dapat mengurangi emisi karbon dari transportasi jarak jauh.\n* **Pilih produk organik:** Produk organik biasanya dihasilkan melalui praktik berkelanjutan yang lebih ramah lingkungan.\n* **Kurangi pemborosan makanan:** Mengurangi pemborosan makanan, termasuk produk hewani, merupakan langkah penting dalam mengurangi emisi karbon.\n\n**Ajakan untuk Berkelanjutan:**\n\nJejak karbon dari konsumsi makanan adalah salah satu kontributor besar terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. Mari kita berkontribusi dalam menjaga bumi ini dengan memilih makanan yang mendukung keberlanjutan dan mengurangi jejak karbon dari konsumsi kita sehari-hari. \n",
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
                "Jejak karbon dari 1 kg beras adalah sekitar **4.45 kg CO2e**.\n\nRincian emisi:\n\n* **Pertanian:** 3.553953627 kg CO2e\n* **Pengolahan:** 0.065220036 kg CO2e\n* **Transportasi:** 0.095619114 kg CO2e\n* **Ritel:** 0.063362152 kg CO2e\n* **Pengemasan:** 0.083853899 kg CO2e\n* **Kerugian:** 0.611516643 kg CO2e\n* **Penggunaan Lahan:** -0.02187964 kg CO2e (dampak negatif terhadap lingkungan)\n\nSaran praktis:\n\n* **Pilih varietas beras lokal:** Mengonsumsi varietas beras lokal dapat mengurangi emisi karbon dari transportasi jarak jauh.\n* **Kurangi konsumsi beras:** Beras memiliki jejak karbon yang relatif tinggi dibandingkan dengan serealia lainnya seperti gandum dan jagung.\n* **Pilih beras organik:** Produk organik biasanya dihasilkan melalui praktik berkelanjutan yang lebih ramah lingkungan.\n* **Kurangi pemborosan makanan:** Mengurangi pemborosan makanan, termasuk beras, merupakan langkah penting dalam mengurangi emisi karbon.\n\nJejak karbon dari konsumsi makanan adalah salah satu kontributor besar terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. Mari kita berkontribusi dalam menjaga bumi ini dengan memilih makanan yang mendukung keberlanjutan dan mengurangi jejak karbon dari konsumsi kita sehari-hari. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "cheese ",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Jejak karbon dari 1 kg keju adalah sekitar **13.09 kg CO2e**. \n\nRincian emisi:\n\n* **Pertanian:** 13.0955392 kg CO2e\n* **Pengolahan:** 0.740386293 kg CO2e\n* **Transportasi:** 0.138556663 kg CO2e\n* **Ritel:** 0.333337741 kg CO2e\n* **Pengemasan:** 0.172090931 kg CO2e\n* **Kerugian:** 2.577136521 kg CO2e\n* **Penggunaan Lahan:** 4.467476309 kg CO2e (dampak negatif terhadap lingkungan)\n\nSaran praktis:\n\n* **Kurangi konsumsi keju:** Keju memiliki jejak karbon yang relatif tinggi dibandingkan dengan produk susu lainnya. \n* **Pilih keju lokal:** Mengonsumsi keju yang diproduksi secara lokal dapat mengurangi emisi karbon dari transportasi jarak jauh.\n* **Pilih keju organik:** Produk organik biasanya dihasilkan melalui praktik berkelanjutan yang lebih ramah lingkungan.\n* **Kurangi pemborosan makanan:** Mengurangi pemborosan makanan, termasuk keju, merupakan langkah penting dalam mengurangi emisi karbon.\n\nJejak karbon dari konsumsi makanan adalah salah satu kontributor besar terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. Mari kita berkontribusi dalam menjaga bumi ini dengan memilih makanan yang mendukung keberlanjutan dan mengurangi jejak karbon dari konsumsi kita sehari-hari. \n",
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
                "Jejak karbon dari 1 buah pisang adalah sekitar **0.74 kg CO2e**. \n\nRincian emisi:\n\n* **Pertanian:** 0.269618358 kg CO2e\n* **Pengolahan:** 0.06014592 kg CO2e\n* **Transportasi:** 0.295830362 kg CO2e\n* **Ritel:** 0.020980708 kg CO2e\n* **Pengemasan:** 0.065670278 kg CO2e\n* **Kerugian:** 0.175184627 kg CO2e\n* **Penggunaan Lahan:** -0.025533871 kg CO2e (dampak negatif terhadap lingkungan)\n\nSaran praktis:\n\n* **Beli pisang secukupnya:** Mengurangi pemborosan makanan turut membantu menurunkan emisi karbon secara signifikan.\n* **Pilih pisang lokal:** Mengonsumsi makanan yang diproduksi secara lokal dapat mengurangi emisi karbon dari transportasi jarak jauh.\n* **Pilih pisang organik:** Produk organik biasanya dihasilkan melalui praktik berkelanjutan yang lebih ramah lingkungan.\n* **Gunakan kemasan ramah lingkungan:** Pilih pisang yang dikemas dengan bahan yang dapat didaur ulang atau diurai oleh alam (kompos).\n\nJejak karbon dari konsumsi makanan adalah salah satu kontributor besar terhadap perubahan iklim. Dengan memahami emisi karbon dari makanan yang kita konsumsi, kita dapat membuat pilihan yang lebih berkelanjutan dan membantu mengurangi dampak kita terhadap lingkungan. Mari kita berkontribusi dalam menjaga bumi ini dengan memilih makanan yang mendukung keberlanjutan dan mengurangi jejak karbon dari konsumsi kita sehari-hari. \n",
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
