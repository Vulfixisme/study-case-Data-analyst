"""
transform.py
------------
Pipeline transformasi data wide -> tidy untuk Study Case 2 (Data Analyst).
Dipakai baik oleh notebook (Riliv_Data_Cleaning.ipynb) maupun oleh dashboard
Streamlit (dashboard_app.py), supaya logikanya konsisten di satu tempat.
"""

import re
import numpy as np
import pandas as pd
from mapping import QUESTION_MAPPING, normalize_label, FINAL_COLUMN_ORDER

RAW_PATH = "data/Raw_Data.xlsx"


# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------
def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="raw")
    return df


# ---------------------------------------------------------------------------
# 2. WIDE -> LONG -> WIDE-TIDY (pivot berdasarkan kategori mapping)
# ---------------------------------------------------------------------------
def melt_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """Ubah 10 pasang kolom Question/Response menjadi format panjang (long),
    satu baris = satu pasangan question-response yang terisi."""
    df = df.reset_index().rename(columns={"index": "row_id"})
    records = []
    for i in range(1, 11):
        qcol, rcol = f"Question {i}", f"Response {i}"
        sub = df[["row_id", "Invitee Name", "Start Date & Time", "End Date & Time",
                   "Event Created Date & Time", qcol, rcol]].copy()
        sub = sub.rename(columns={qcol: "Question", rcol: "Response"})
        sub["slot"] = i
        records.append(sub)
    long_df = pd.concat(records, ignore_index=True)
    # buang baris yang question-nya kosong (tidak ada pertanyaan di slot ini)
    long_df = long_df[long_df["Question"].notna()].copy()
    long_df["Question_norm"] = long_df["Question"].apply(normalize_label)
    long_df["Category"] = long_df["Question_norm"].map(QUESTION_MAPPING).fillna("Other_Info")
    return long_df


def pivot_to_tidy(long_df: pd.DataFrame, raw_df: pd.DataFrame) -> pd.DataFrame:
    """Pivot dari long -> satu baris per pendaftaran (row_id), satu kolom per kategori.
    Jika dalam satu baris ada >1 Response yang jatuh ke kategori yang sama
    (misal 2 variasi pertanyaan Consent terisi sekaligus), nilai-nilainya
    digabung dengan ' | ' supaya tidak ada data yang hilang."""

    def combine(vals):
        vals = [str(v).strip() for v in vals if pd.notna(v) and str(v).strip() != ""]
        vals = list(dict.fromkeys(vals))  # unique, keep order
        return " | ".join(vals) if vals else np.nan

    pivot = (
        long_df.groupby(["row_id", "Category"])["Response"]
        .apply(combine)
        .unstack("Category")
    )

    meta = raw_df[["Invitee Name", "Start Date & Time", "End Date & Time",
                    "Event Created Date & Time"]].copy()
    meta.index.name = "row_id"
    tidy = meta.join(pivot)
    tidy = tidy.reset_index(drop=True)
    return tidy


# ---------------------------------------------------------------------------
# 3. CLEANING TAMBAHAN
# ---------------------------------------------------------------------------
def clean_usia(val):
    """Ambil angka usia dari teks bebas ('25', '25 tahun', '25.0') -> int.
    Nilai di luar rentang wajar (10-100 tahun) dianggap salah input dan
    diubah jadi NaN (contoh ditemukan di data: tahun lahir '1989', atau angka
    besar semacam nomor telepon/timestamp yang salah ketik ke kolom usia)."""
    if pd.isna(val):
        return np.nan
    m = re.search(r"\d+", str(val))
    if not m:
        return np.nan
    age = int(m.group())
    if age < 10 or age > 100:
        return np.nan
    return age


def clean_gender(val):
    if pd.isna(val):
        return np.nan
    v = str(val).strip().lower()
    if v in ("laki-laki", "laki laki", "pria", "male", "m", "l"):
        return "Laki-laki"
    if v in ("perempuan", "wanita", "female", "f", "p"):
        return "Perempuan"
    return str(val).strip().title()


def clean_text_titlecase(val):
    if pd.isna(val):
        return np.nan
    v = str(val).strip()
    return v if v == "" else v[:1].upper() + v[1:]


def standardize_perusahaan(val):
    if pd.isna(val):
        return np.nan
    return str(val).strip().upper()


def clean_status_kepegawaian(val):
    if pd.isna(val):
        return np.nan
    v = str(val).strip().lower()
    if "keluarga" in v and "karyawan" not in v.split("keluarga")[0]:
        pass
    if v.startswith("karyawan") or v == "karyawan":
        return "Karyawan"
    if "keluarga" in v:
        return "Keluarga Karyawan"
    return str(val).strip().title()


def apply_cleaning(tidy: pd.DataFrame) -> pd.DataFrame:
    tidy = tidy.copy()

    if "Usia" in tidy.columns:
        tidy["Usia"] = tidy["Usia"].apply(clean_usia)

    if "Gender" in tidy.columns:
        tidy["Gender"] = tidy["Gender"].apply(clean_gender)

    if "Perusahaan" in tidy.columns:
        tidy["Perusahaan"] = tidy["Perusahaan"].apply(standardize_perusahaan)

    if "Status_Kepegawaian" in tidy.columns:
        tidy["Status_Kepegawaian"] = tidy["Status_Kepegawaian"].apply(clean_status_kepegawaian)

    for col in ["Divisi_Departemen", "Topik_Permasalahan", "Jenis_Layanan_Konseling",
                "Bahasa_Konsultasi", "Sumber_Informasi"]:
        if col in tidy.columns:
            tidy[col] = tidy[col].apply(clean_text_titlecase)

    # tandai sesi lanjutan: baris yang HANYA berisi kode sesi konseling
    # (tidak ada info substantif lain terisi)
    info_cols = [c for c in tidy.columns if c not in
                 ("Invitee Name", "Start Date & Time", "End Date & Time",
                  "Event Created Date & Time", "Kode_Sesi_Konseling", "Share_ID")]
    tidy["Is_Continuation_Session"] = tidy[info_cols].isna().all(axis=1)

    # urutkan kolom sesuai FINAL_COLUMN_ORDER (kolom yang tidak muncul di data diabaikan)
    ordered_cols = [c for c in FINAL_COLUMN_ORDER if c in tidy.columns]
    remaining = [c for c in tidy.columns if c not in ordered_cols]
    tidy = tidy[ordered_cols + remaining]

    # format tanggal jadi kolom terpisah yang gampang dipakai dashboard
    tidy["Tanggal_Sesi"] = pd.to_datetime(tidy["Start Date & Time"]).dt.date
    tidy["Bulan_Sesi"] = pd.to_datetime(tidy["Start Date & Time"]).dt.to_period("M").astype(str)

    return tidy


# ---------------------------------------------------------------------------
# 4. PIPELINE UTUH
# ---------------------------------------------------------------------------
def run_pipeline(path: str = RAW_PATH):
    raw = load_raw(path)
    long_df = melt_to_long(raw)
    tidy = pivot_to_tidy(long_df, raw)
    tidy_clean = apply_cleaning(tidy)
    return raw, long_df, tidy_clean


if __name__ == "__main__":
    raw, long_df, tidy = run_pipeline()
    print("Raw:", raw.shape)
    print("Long:", long_df.shape)
    print("Tidy:", tidy.shape)
    print(tidy.head(3).to_string())
