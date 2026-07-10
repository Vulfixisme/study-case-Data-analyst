"""
mapping.py
----------
Kamus pemetaan (mapping dictionary) dari seluruh variasi label pertanyaan
(kolom 'Question 1' .. 'Question 10') ke nama kolom standar hasil (tidy).

Dibangun dari eksplorasi seluruh 121 label unik yang ditemukan di dataset
(lihat notebook, Bagian 2 - Eksplorasi Data).

Cara pakai:
    from mapping import QUESTION_MAPPING, normalize_label
    category = QUESTION_MAPPING.get(normalize_label(question_text), "Other_Info")
"""

import re

def normalize_label(text: str) -> str:
    """Normalisasi label pertanyaan supaya variasi kecil (spasi ganda, newline,
    emoji peringatan, capitalisasi) tidak dianggap label yang berbeda."""
    if text is None:
        return ""
    t = str(text)
    t = t.replace("\\n", "\n")            # handle literal backslash-n if present
    t = t.replace("\n", " ").replace("\r", " ")
    t = re.sub(r"\s+", " ", t)             # collapse whitespace
    t = t.strip()
    return t

# --------------------------------------------------------------------------
# KAMUS MAPPING: normalized_label -> kategori_kolom_hasil
# --------------------------------------------------------------------------
QUESTION_MAPPING = {}

def _add(category, labels):
    for lbl in labels:
        QUESTION_MAPPING[normalize_label(lbl)] = category

# 1. PERUSAHAAN -------------------------------------------------------------
_add("Perusahaan", [
    "Kode Perusahaan",
    "Kode perusahaan",
    "Kode perusahaan (⚠️Jangan diganti!)",
    "Company Code",
    "Company code",
    "Nama Perusahaan",
    "Nama perusahaan",
    "Nama Perusahaan (Mohon tulis lengkap sesuai dengan nama PT dan Unit Anda)",
    "Business Entity",
    "Perusahaan",
])

# 2. DIVISI / DEPARTEMEN -----------------------------------------------------
_add("Divisi_Departemen", [
    "Divisi",
    "Departemen",
    "Work Division",
    "Work division",
    "Divisi/Unit Kerja",
    "Unit Kerja",
    "Unit Kerja (dari karyawan yang bekerja)",
    "Departemen/Divisi",
    "Divisi (dari karyawan yang bekerja)",
])

# 3. USIA --------------------------------------------------------------------
_add("Usia", [
    "Usia",
    "usia",
    "Age",
])

# 4. GENDER --------------------------------------------------------------------
_add("Gender", [
    "Gender",
    "Jenis Kelamin",
])

# 5. JENIS LAYANAN KONSELING --------------------------------------------------
_add("Jenis_Layanan_Konseling", [
    "Pilihan layanan konseling",
    "Pilihan Layanan Konseling",
    "Pilih layanan konseling",
    "Counselling Service of Choice",
    "Counseling Service of Choice",
    "Metode konseling",
    "Metode Konseling",
    "Layanan konseling",
    "Tipe Konseling",
    "Pilihan layanan konsultasi",
])

# 6. TOPIK PERMASALAHAN --------------------------------------------------------
_add("Topik_Permasalahan", [
    "Topik permasalahan yang ingin dibahas pada sesi konseling",
    "Topik permasalahan yang ingin dibahas dalam sesi konseling",
    "Topik permasalahan yang ingin dibahas pada sesi konsultasi",
    "Topik Permasalahan yang Ingin dibahas Pada Sesi Konsultasi",
    "Topik Permasalahan yang ingin dibahas",
    "Topik Konsultasi",
    "Counselling Topic",
    "Counselling topic",
    "Topik",
])

# 7. GAMBARAN SINGKAT MASALAH ---------------------------------------------------
_add("Gambaran_Singkat_Masalah", [
    "Gambaran singkat permasalahan",
    "Gambaran Singkat Permasalahan",
    "Gambaran singkat permasalahan (Opsional)",
    "Gambaran permasalahan",
    "Give a brief explanation of problem you would like to talk in the session",
    "Please share anything that will help prepare for our meeting.",
])

# 8. SUMBER INFORMASI ------------------------------------------------------------
_add("Sumber_Informasi", [
    "Dari mana Anda mengetahui informasi pendaftaran program kesehatan mental?",
    "How did you find out about this mental health program?",
    "Dari mana Anda mengetahui informasi pendaftaran program konsultasi finansial?",
    "Dari mana Anda mengetahui informasi pendaftaran program konsultasi nutrisi?",
    "Dari mana Anda mengetahui program BREATHE dari Danone inil?",
])

# 9. STATUS KEPEGAWAIAN -----------------------------------------------------------
_add("Status_Kepegawaian", [
    "Apakah Anda mendaftar sebagai karyawan atau keluarga karyawan?",
    "Apakah Anda mendaftar sebagai karyawan atau keluarga karyawan? Jika Anda mendaftar sebagai keluarga, mohon sebutkan nama karyawan yang terdaftar.",
    "Apakah Anda mendaftar sebagai karyawan atau keluarga karyawan? Jika Anda mendaftar sebagai keluarga, mohon sebutkan nama karyawan yang terdaftar",
    "Status Kepegawaian",
    "Apakah Anda karyawan PKT atau anggota keluarga dari karyawan PKT?",
    "Apakah Anda karyawan dari perusahaan tersebut atau anggota keluarga dari karyawan perusahaan?",
    "Mendaftar sebagai?",
])

# 10. NAMA KARYAWAN TERKAIT (jika mendaftar sbg keluarga) -------------------------
_add("Nama_Karyawan_Terkait_Keluarga", [
    "Jika Anda mendaftar sebagai keluarga, mohon sebutkan nama karyawan yang terdaftar.",
    "Jika Anda mendaftar sebagai keluarga, mohon sebutkan nama karyawan yang terdaftar (kosongi jika Anda bukan anggota keluarga)",
    "Jika Anda mendaftar sebagai keluarga, mohon sebutkan nama karyawan yang terdaftar",
    "Jika Anda mendaftar sebagai keluarga, mohon sebutkan nama karyawan yang terdaftar. Jika sebagai karyawan, dikosongi saja.",
    "Jika Anda mendaftar sebagai keluarga, mohon sebutkan nama karyawan PKT yang terdaftar (Jika Anda karyawan PKT, bisa dikosongi)",
    "Jika Anda adalah anggota keluarga, tulis nama karyawan yang memiliki hubungan keluarga di PKT. Jika bukan anggota keluarga, dikosongi saja",
    "Jika Anda adalah anggota keluarga, tulis nama karyawan yang memiliki hubungan keluarga di perusahaan tersebut. Jika bukan anggota keluarga, dikosongi saja.",
    "Mohon tuliskan nama anggota keluarga yang bekerja di perusahaan ini beserta hubungannya (contoh penulisan: Anak dari Budi Hermawan). Jika tidak ada, kosongkan bagian ini.",
    "Mohon tuliskan nama anggota keluarga yang bekerja di perusahaan ini beserta hubungannya (contoh penulisan: Budi – Anak). Jika tidak ada, kosongkan bagian ini.",
    "Nama karyawan yang bekerja pada perusahaan",
    "Hubungan peserta dengan karyawan",
    "Status hubungan",
])

# 11. BAHASA KONSULTASI -------------------------------------------------------------
_add("Bahasa_Konsultasi", [
    "Bahasa yang digunakan saat konsultasi",
    "In which language would you like to have your counseling session? (If you choose English, please select Psychologist Amira Eka Pratiwi)",
])

# 12. PERSETUJUAN DATA (INFORMED CONSENT) -------------------------------------------
_add("Persetujuan_Data_Consent", [
    "Dalam program konseling bersama Riliv, ringkasan permasalahan yang Anda ceritakan kepada Psikolog Riliv selama sesi konseling akan disampaikan ke perusahaan dengan tetap menjaga kerahasiaan nama Anda. Apakah Anda bersedia?",
    "Dalam program konseling bersama Riliv, ringkasan permasalahan yang Anda ceritakan kepada CFP Riliv selama sesi konseling akan disampaikan ke perusahaan dengan tetap menjaga kerahasiaan nama Anda. Apakah Anda bersedia?",
    "Dalam program konsultasi bersama Riliv, ringkasan permasalahan yang Anda ceritakan kepada Nutritionist Riliv selama sesi konsultasi akan disampaikan ke perusahaan dengan tetap menjaga kerahasiaan nama Anda. Apakah Anda bersedia?",
    "Dalam program konseling bersama Riliv, hasil konseling yang Anda ceritakan kepada Psikolog Riliv selama sesi konseling akan disampaikan ke perusahaan dalam bentuk dokumen laporan. Apakah Anda bersedia?",
    "During the Riliv counselling program, the brief summary of your problems discussed with the Riliv's Psychologist will be submitted to the company anonymously. Do you agree to submit the brief summary of your session?",
    "Sebelum melanjutkan proses pendaftaran, harap baca dan pahami Informed Consent (IC) yang telah kami tampilkan di kiri halaman ini (tampilan web) atau di deskripsi atas (tampilan ponsel). Kemudian silakan pilih salah satu opsi berikut:",
    "Sebelum melanjutkan proses pendaftaran, harap baca dan pahami Informed Consent (IC) yang telah kami tampilkan di kiri halaman ini (tampilan web) atau di deskripsi atas (tampilan ponsel). Kemudian silakan pilih salah satu opsi berikut:",
    "Sebelum melanjutkan proses pendaftaran, harap baca dan pahami Informed Consent (IC) yang telah kami sediakan melalui tautan berikut: https://bit.ly/InformedConsent-Konseling-RilivforCompany Silakan pilih salah satu opsi berikut:",
    "Before proceeding with the registration process, please read and understand the Informed Consent (IC) displayed on the left side of this page (web view) or in the description above (mobile view). Then, please select one of the following options:",
    "Before proceeding with the registration process, please read and understand the Informed Consent (IC) that we have provided on the left side of this page (web view) or at the top description (mobile view). Then, please select one of the following options:",
    "Dengan ini, saya menyatakan kesediaan saya bahwa ringkasan permasalahan yang saya ceritakan kepada Psikolog Riliv selama sesi konseling akan disampaikan ke perusahaan.",
    "Sebelum melanjutkan proses pendaftaran, harap baca dan pahami Informed Consent (IC) yang telah kami sediakan melalui tautan berikut: https://bit.ly/InformedConsent-Konseling-RilivforCompany. Silakan pilih salah satu opsi berikut:",
])

# 24. DATA KOTOR / TIDAK VALID (ditemukan saat eksplorasi) ----------------------------------
# Label ini kemungkinan hasil kesalahan input pada form (isi Question berupa nama layanan,
# bukan pertanyaan; Response-nya pun berisi data uji seperti "60", "ywyys", "Testing").
# Tetap dipetakan (bukan dibuang) supaya bisa ditelusuri di kolom Other_Info.
_add("Other_Info", [
    "Konseling Psikologi Video Call - 60'",
])

# 13. KODE SESI KONSELING (Counseling/Consultation Code) -----------------------------
_add("Kode_Sesi_Konseling", [
    "Counseling Code",
    "Counseling Code (terisi otomatis - tidak untuk diubah/diedit)",
    "Consultation Code (⚠️mohon jangan diganti atau diubah)",
    "Consultation Code",
    "Kode Konseling (⚠️Jangan diganti!)",
])

# 14. SHARE ID -------------------------------------------------------------------------
_add("Share_ID", ["Share ID"])

# 15. NOMOR WHATSAPP ----------------------------------------------------------------------
_add("Nomor_WhatsApp", [
    "No. Handphone (Whatsapp aktif)",
    "Nomor Whattsapp",
    "Nomor Whatssapp",
    "Nomor Whatsapp",
    "Nomor WhatsApp",
    "Nomor Whatsapp Aktif",
])

# 16. NIK ---------------------------------------------------------------------------------
_add("NIK", ["NIK"])

# 17. DATA KESEHATAN FISIK (tinggi/berat badan, lingkar pinggang, durasi tidur) ------------
_add("Data_Kesehatan_Fisik", [
    "Tinggi Badan (dalam cm) dan Berat Badan (dalam kg)",
    "Tinggi Badan (cm) dan Berat Badan (cm)",
    "Tinggi Badan (cm) dan Berat Badan (kg)",
    "Usia (tahun), Tinggi Badan (cm) dan Berat Badan (kg)",
    "Tinggi Badan (dalam cm)",
    "Berat Badan (dalam kg)",
    "Lingkar pinggang (cm)",
    "Durasi tidur rata-rata perhari (jam)",
])

# 18. JENIS OLAHRAGA ------------------------------------------------------------------------
_add("Jenis_Olahraga", [
    "Jenis Olahraga dan frekuensinya dalam seminggu (Jika tidak olahraga harap diisi \"tidak berolahraga\")",
    "Jenis Olahraga dan frekuensinya dalam seminggu (Jika tidak olahraga harap diisi \"tidak berolahraga\") Jenis Olahraga dan frekuensinya dalam seminggu (Jika tidak olahraga harap diisi \"tidak berolahraga\")",
])

# 19. ALERGI & RIWAYAT PENYAKIT -----------------------------------------------------------
_add("Alergi_Riwayat_Penyakit", [
    "Alergi dan riwayat penyakit lainnya (Jika tidak ada, harap diisi \"tidak ada\")",
    "Alergi dan riwayat penyakit lainnya (Jika tidak ada, bisa diisi \"tidak ada alergi\")",
    "Alergi dan riwayat penyakit lainnya (Jika tidak ada, bisa dikosongi\")",
])

# 20. KONSELING KECANDUAN ROKOK ------------------------------------------------------------
_add("Konseling_Kecanduan_Rokok", [
    "Apakah kamu ingin melakukan konseling terkait kecanduan rokok?",
    "Apakah Anda ingin melakukan konseling terkait kecanduan rokok?",
])

# 21. POSISI / JABATAN -----------------------------------------------------------------------
_add("Posisi_Jabatan", ["Posisi"])

# 22. FACTORY & AREA (khusus klien manufaktur) ------------------------------------------------
_add("Factory_Area", ["Factory dan Area"])

# 23. TIPE PROGRAM NUTRISI ----------------------------------------------------------------------
_add("Tipe_Program_Nutrisi", ["Tipe Program Nutrisi yang Dipilih"])

# --------------------------------------------------------------------------
# Kategori final yang akan menjadi KOLOM pada tabel tidy (urutan tampil)
# --------------------------------------------------------------------------
FINAL_COLUMN_ORDER = [
    "Invitee Name",
    "Start Date & Time",
    "End Date & Time",
    "Event Created Date & Time",
    "Is_Continuation_Session",
    "Kode_Sesi_Konseling",
    "Share_ID",
    "Perusahaan",
    "Divisi_Departemen",
    "Posisi_Jabatan",
    "Factory_Area",
    "Usia",
    "Gender",
    "Status_Kepegawaian",
    "Nama_Karyawan_Terkait_Keluarga",
    "Nomor_WhatsApp",
    "NIK",
    "Jenis_Layanan_Konseling",
    "Bahasa_Konsultasi",
    "Topik_Permasalahan",
    "Gambaran_Singkat_Masalah",
    "Konseling_Kecanduan_Rokok",
    "Tipe_Program_Nutrisi",
    "Data_Kesehatan_Fisik",
    "Jenis_Olahraga",
    "Alergi_Riwayat_Penyakit",
    "Sumber_Informasi",
    "Persetujuan_Data_Consent",
    "Other_Info",
]
