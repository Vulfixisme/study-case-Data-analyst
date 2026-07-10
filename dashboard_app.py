"""
dashboard_app.py
-----------------
Dashboard reporting bulanan untuk data pendaftaran konseling (Study Case 2).
Jalankan dengan:  streamlit run dashboard_app.py

Data yang ditampilkan dihasilkan oleh pipeline yang sama dengan notebook
(`transform.py` + `mapping.py`), sehingga logikanya konsisten satu sumber.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from transform import run_pipeline

st.set_page_config(
    page_title="Riliv Counseling — Dashboard Reporting",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------------------------
# LOAD DATA (cached supaya pipeline transformasi tidak dijalankan ulang
# setiap kali user berinteraksi dengan filter)
# ---------------------------------------------------------------------------
@st.cache_data
def get_data():
    _, _, tidy = run_pipeline()
    tidy["Start Date & Time"] = pd.to_datetime(tidy["Start Date & Time"])
    return tidy


df = get_data()

st.title("📊 Dashboard Reporting — Pendaftaran Konseling")
st.caption(
    "Data telah melalui proses cleaning & transformasi wide → tidy "
    "(lihat notebook `Riliv_Data_Cleaning_Dashboard.ipynb` untuk detail prosesnya)."
)

# ---------------------------------------------------------------------------
# SIDEBAR — FILTER
# ---------------------------------------------------------------------------
st.sidebar.header("🔎 Filter")

exclude_continuation = st.sidebar.checkbox(
    "Sembunyikan sesi lanjutan (data kosong)", value=True,
    help="Baris yang hanya berisi kode sesi tanpa detail lain (kemungkinan sesi lanjutan)."
)

work_df = df.copy()
if exclude_continuation:
    work_df = work_df[~work_df["Is_Continuation_Session"]]

companies = sorted(work_df["Perusahaan"].dropna().unique().tolist())
selected_companies = st.sidebar.multiselect("Perusahaan", options=companies, default=[])

min_date, max_date = work_df["Start Date & Time"].min(), work_df["Start Date & Time"].max()
date_range = st.sidebar.date_input(
    "Rentang tanggal sesi",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date(),
)

if selected_companies:
    work_df = work_df[work_df["Perusahaan"].isin(selected_companies)]

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
    work_df = work_df[
        (work_df["Start Date & Time"].dt.date >= start_d)
        & (work_df["Start Date & Time"].dt.date <= end_d)
    ]

st.sidebar.markdown("---")
st.sidebar.metric("Baris setelah filter", f"{len(work_df):,}")

# ---------------------------------------------------------------------------
# KPI ROW
# ---------------------------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Pendaftaran", f"{len(work_df):,}")
k2.metric("Jumlah Perusahaan", f"{work_df['Perusahaan'].nunique():,}")
k3.metric("Rata-rata Usia", f"{work_df['Usia'].mean():.1f} th" if work_df['Usia'].notna().any() else "-")
consent_yes_rate = (
    work_df["Persetujuan_Data_Consent"].astype(str).str.contains("bersedia", case=False, na=False)
    & ~work_df["Persetujuan_Data_Consent"].astype(str).str.contains("tidak", case=False, na=False)
)
k4.metric("Tingkat Persetujuan Data", f"{consent_yes_rate.mean()*100:.0f}%" if len(work_df) else "-")
k5.metric("Sesi Lanjutan (raw)", f"{df['Is_Continuation_Session'].sum():,}")

st.markdown("---")

# ---------------------------------------------------------------------------
# ROW 1 — Tren waktu & Top perusahaan
# ---------------------------------------------------------------------------
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("Tren Jumlah Pendaftaran per Bulan")
    monthly = (
        work_df.groupby(work_df["Start Date & Time"].dt.to_period("M").astype(str))
        .size()
        .reset_index(name="Jumlah Pendaftaran")
        .rename(columns={"Start Date & Time": "Bulan"})
        .sort_values("Bulan")
    )
    fig = px.line(monthly, x="Bulan", y="Jumlah Pendaftaran", markers=True)
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Top 10 Perusahaan")
    top_comp = work_df["Perusahaan"].value_counts().head(10).sort_values()
    fig = px.bar(top_comp, orientation="h", labels={"value": "Jumlah", "index": "Perusahaan"})
    fig.update_layout(height=380, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# ROW 2 — Demografi
# ---------------------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.subheader("Distribusi Usia")
    if work_df["Usia"].notna().any():
        fig = px.histogram(work_df, x="Usia", nbins=20)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data usia pada rentang filter ini.")

with c4:
    st.subheader("Distribusi Gender")
    gender_counts = work_df["Gender"].value_counts()
    if len(gender_counts):
        fig = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index, hole=0.4)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data gender pada rentang filter ini.")

# ---------------------------------------------------------------------------
# ROW 3 — Topik & Layanan
# ---------------------------------------------------------------------------
c5, c6 = st.columns(2)

with c5:
    st.subheader("Topik Permasalahan Terbanyak")
    top_topic = work_df["Topik_Permasalahan"].value_counts().head(10).sort_values()
    if len(top_topic):
        fig = px.bar(top_topic, orientation="h", labels={"value": "Jumlah Sesi", "index": "Topik"})
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data topik pada rentang filter ini.")

with c6:
    st.subheader("Jenis Layanan Konseling")
    service_counts = work_df["Jenis_Layanan_Konseling"].value_counts().head(10).sort_values()
    if len(service_counts):
        fig = px.bar(service_counts, orientation="h", labels={"value": "Jumlah", "index": "Layanan"})
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data layanan pada rentang filter ini.")

# ---------------------------------------------------------------------------
# ROW 4 — Status kepegawaian & Divisi
# ---------------------------------------------------------------------------
c7, c8 = st.columns(2)

with c7:
    st.subheader("Status Kepegawaian")
    status_counts = work_df["Status_Kepegawaian"].value_counts()
    if len(status_counts):
        fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, hole=0.4)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data status kepegawaian pada rentang filter ini.")

with c8:
    st.subheader("Top 10 Divisi / Departemen")
    top_div = work_df["Divisi_Departemen"].value_counts().head(10).sort_values()
    if len(top_div):
        fig = px.bar(top_div, orientation="h", labels={"value": "Jumlah", "index": "Divisi"})
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data divisi pada rentang filter ini.")

# ---------------------------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("📋 Data Tidy (setelah filter)")
display_cols = [
    "Invitee Name", "Start Date & Time", "Perusahaan", "Divisi_Departemen", "Usia", "Gender",
    "Status_Kepegawaian", "Jenis_Layanan_Konseling", "Topik_Permasalahan",
    "Persetujuan_Data_Consent", "Is_Continuation_Session",
]
display_cols = [c for c in display_cols if c in work_df.columns]
st.dataframe(work_df[display_cols], use_container_width=True, height=350)

st.download_button(
    "⬇️ Download data tidy (CSV) hasil filter",
    data=work_df.to_csv(index=False).encode("utf-8"),
    file_name="tidy_data_filtered.csv",
    mime="text/csv",
)
