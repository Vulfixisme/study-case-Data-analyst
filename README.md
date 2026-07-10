# Study Case 2 — Data Cleaning, Transformasi & Dashboard (Riliv Counseling)

## Isi folder
- `Riliv_Data_Cleaning_Dashboard.ipynb` — notebook utama: eksplorasi, mapping, transformasi wide→tidy, cleaning, dan EDA (sudah dijalankan, hasil/output tersimpan di dalam notebook).
- `mapping.py` — kamus mapping seluruh variasi label pertanyaan → kolom standar.
- `transform.py` — pipeline transformasi (dipakai bareng oleh notebook & dashboard, biar konsisten).
- `dashboard_app.py` — dashboard interaktif **Streamlit**.
- `data/Raw_Data.xlsx` — data mentah asli (sheet `raw`).
- `data/1_raw_data.csv`, `data/2_long_format_mapping.csv`, `data/3_tidy_final.csv` — 3 tahap proses (raw → long/mapping → tidy final) dalam format CSV.
- `data/Riliv_Data_Cleaning_Result.xlsx` — seluruh proses (raw, kamus mapping, long format, tidy final) dalam satu workbook, tiap tahap 1 sheet.

## Cara menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Buka notebook
```bash
jupyter notebook Riliv_Data_Cleaning_Dashboard.ipynb
```
(Notebook sudah dijalankan sebelumnya — semua output/chart sudah tampil. Bisa dijalankan ulang dengan Run All jika ingin memverifikasi.)

### 3. Jalankan dashboard Streamlit
```bash
streamlit run dashboard_app.py
```
Dashboard akan otomatis membaca & memproses `data/Raw_Data.xlsx` lewat pipeline yang sama dengan notebook (`transform.py`), lalu menampilkan KPI, filter perusahaan/tanggal, dan berbagai chart interaktif (tren pendaftaran bulanan, distribusi usia/gender, top perusahaan, topik permasalahan, jenis layanan, status kepegawaian, divisi).

## Ringkasan pendekatan
1. Kumpulkan seluruh label unik di kolom `Question 1..10` (ditemukan 121 variasi).
2. Kelompokkan variasi label tersebut ke 24 kategori kolom standar (kamus di `mapping.py`), berdasarkan kemiripan makna.
3. Ubah data wide → long (satu baris = satu pasangan question-response) → pivot jadi tidy (satu baris = satu pendaftaran, satu kolom = satu kategori informasi).
4. Bersihkan format usia, gender, nama perusahaan, status kepegawaian, dan tandai baris "sesi lanjutan" yang datanya kosong.
5. Sajikan insight lewat EDA di notebook & dashboard interaktif Streamlit.
