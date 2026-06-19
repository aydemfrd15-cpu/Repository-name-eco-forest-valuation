import streamlit as st
import pandas as pd
from PIL import Image
import re

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Eco-Forest Valuation KPH Cepu",
    page_icon="🌳",
    layout="wide"
)

# =====================================================
# LOAD LOGO
# =====================================================

logo = Image.open("Logo Unisbaa.png")

# =====================================================
# LOAD EXCEL
# =====================================================

profil_hutan = pd.read_excel(
    "df_forest_profile.xlsx",
    header=4
)

produksi_kayu = pd.read_excel(
    "df_wood_production.xlsx",
    header=3
)

master_data = pd.read_excel(
    "df_master_data.xlsx",
    header=3
)

parameter = pd.read_excel(
    "df_simulation_params.xlsx",
    header=3
)

dashboard = pd.read_excel(
    "df_dashboard_summary.xlsx",
    header=3
)

# =====================================================
# FUNGSI EKSTRAK ANGKA
# =====================================================

def extract_number(value):

    if pd.isna(value):
        return None

    text = str(value)

    match = re.search(
        r"[-+]?\d*\.?\d+",
        text.replace(",", "")
    )

    if match:
        return float(match.group())

    return None


# =====================================================
# FUNGSI GRAFIK
# =====================================================

def create_chart_from_table(df, label_col, value_col, title):

    try:

        chart_df = df[[label_col, value_col]].copy()

        chart_df[value_col] = chart_df[value_col].apply(
            extract_number
        )

        chart_df = chart_df.dropna()

        if len(chart_df) > 0:

            st.subheader(title)

            st.bar_chart(
                chart_df.set_index(label_col)
            )

    except:
        st.info("Data grafik tidak tersedia.")


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.image(
    logo,
    use_container_width=True
)

st.sidebar.markdown("## Eco-Forest Valuation")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "Beranda",
        "Profil Hutan",
        "Produksi Kayu",
        "Master Data",
        "Parameter Simulasi",
        "Dashboard Summary"
    ]
)

# =====================================================
# BERANDA
# =====================================================

if menu == "Beranda":

    st.title(
        "🌳 Eco-Forest Valuation KPH Cepu (Jawa Tengah)"
    )

    st.caption(
        "PBL 6 — Ekonomi Sumber Daya Hutan"
    )

    st.markdown("---")

    st.markdown("""
### Mata Kuliah
Ekonomi Sumber Daya Alam dan Lingkungan

### Dosen Pengampu
Yuhka Sundaya, S.E., M.Si.
""")

    st.success("""
KELOMPOK 4

• Salsa Zahratul Aulia (10090224004)

• Aida Farida Kultsum (10090224014)

• Nabil Athala Naufal (10090224022)
""")

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Dataset Profil Hutan",
        len(profil_hutan)
    )

    c2.metric(
        "Dataset Produksi",
        len(produksi_kayu)
    )

    c3.metric(
        "Master Data",
        len(master_data)
    )

    c4.metric(
        "Dashboard",
        len(dashboard)
    )

    st.markdown("---")

    st.subheader(
        "Deskripsi Aplikasi"
    )

    st.write("""
Aplikasi ini digunakan untuk analisis ekonomi sumber daya hutan pada kawasan KPH Cepu (Jawa Tengah).

Fitur utama:

• Profil Hutan

• Produksi Kayu

• Master Data

• Parameter Simulasi

• Dashboard Summary

• Visualisasi Data Otomatis

• Analisis Pendukung Valuasi Ekonomi Hutan
""")

# =====================================================
# PROFIL HUTAN
# =====================================================

elif menu == "Profil Hutan":

    st.title("🌳 Profil Hutan KPH Cepu")

    st.dataframe(
        profil_hutan,
        use_container_width=True,
        hide_index=True
    )

    create_chart_from_table(
        profil_hutan,
        "variable",
        "value",
        "Grafik Profil Hutan"
    )

# =====================================================
# PRODUKSI KAYU
# =====================================================

elif menu == "Produksi Kayu":

    st.title("🪵 Produksi Kayu")

    st.dataframe(
        produksi_kayu,
        use_container_width=True,
        hide_index=True
    )

    create_chart_from_table(
        produksi_kayu,
        "Variabel",
        "nilai",
        "Grafik Produksi Kayu"
    )

# =====================================================
# MASTER DATA
# =====================================================

elif menu == "Master Data":

    st.title("📊 Master Data")

    st.info(
        "Master data merupakan basis data yang digunakan dalam analisis ekonomi sumber daya hutan."
    )

    st.dataframe(
        master_data,
        use_container_width=True,
        hide_index=True
    )

    create_chart_from_table(
        master_data,
        "variable",
        "value",
        "Grafik Master Data"
    )

# =====================================================
# PARAMETER SIMULASI
# =====================================================

elif menu == "Parameter Simulasi":

    st.title("⚙️ Parameter Simulasi")

    st.dataframe(
        parameter,
        use_container_width=True,
        hide_index=True
    )

    create_chart_from_table(
        parameter,
        "Parameter",
        "Nilai Awal",
        "Grafik Parameter Simulasi"
    )

# =====================================================
# DASHBOARD SUMMARY
# =====================================================

elif menu == "Dashboard Summary":

    st.title("📈 Dashboard Summary")

    st.dataframe(
        dashboard,
        use_container_width=True,
        hide_index=True
    )

    create_chart_from_table(
        dashboard,
        "Indikator",
        "Nilai",
        "Trade-Off Analysis"
    )

    st.success(
        "Dashboard menampilkan ringkasan valuasi ekonomi hutan, jasa ekosistem, dan trade-off pemanfaatan sumber daya pada kawasan KPH Cepu."
    )