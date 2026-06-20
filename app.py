import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
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
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

[data-testid="stMetric"]{
    border-radius:18px;
    padding:18px;
    border:1px solid rgba(120,120,120,0.20);
    background:rgba(120,120,120,0.08);
}

[data-testid="stMetricLabel"]{
    font-size:1rem;
    font-weight:600;
}

[data-testid="stMetricValue"]{
    font-size:2.2rem;
    font-weight:700;
}

h1,h2,h3{
    font-weight:700;
}

div[data-testid="stDataFrame"]{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD LOGO
# =====================================================

logo = Image.open("Logo Unisbaa.png")

# =====================================================
# CLEAN DATAFRAME
# =====================================================

def clean_dataframe(df):

    df = df.loc[
        :,
        ~df.columns.astype(str).str.contains("^Unnamed")
    ]

    df = df.dropna(
        axis=0,
        how="all"
    )

    df = df.dropna(
        axis=1,
        how="all"
    )

    df.columns = [
        str(col)
        .replace("_", " ")
        .title()
        for col in df.columns
    ]

    return df.reset_index(drop=True)

# =====================================================
# LOAD EXCEL
# =====================================================

profil_hutan = clean_dataframe(
    pd.read_excel(
        "df_forest_profile.xlsx",
        header=4
    )
)

produksi_kayu = clean_dataframe(
    pd.read_excel(
        "df_wood_production.xlsx",
        header=3
    )
)

master_data = clean_dataframe(
    pd.read_excel(
        "df_master_data.xlsx",
        header=3
    )
)

parameter = clean_dataframe(
    pd.read_excel(
        "df_simulation_params.xlsx",
        header=3
    )
)

dashboard = clean_dataframe(
    pd.read_excel(
        "df_dashboard_summary.xlsx",
        header=3
    )
)

# =====================================================
# EKSTRAK ANGKA
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
# GRAFIK PROFESIONAL
# =====================================================

def create_chart_from_table(
    df,
    label_col,
    value_col,
    title
):

    try:

        chart_df = df[
            [label_col, value_col]
        ].copy()

        chart_df[value_col] = (
            chart_df[value_col]
            .apply(extract_number)
        )

        chart_df = chart_df.dropna()

        if len(chart_df) > 0:

            st.subheader(title)

            fig = px.bar(
                chart_df,
                x=label_col,
                y=value_col,
                color=value_col,
                color_continuous_scale="Blues",
                text=value_col
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                height=550,
                showlegend=False,
                xaxis_title="",
                yaxis_title="",
                template="plotly",
                margin=dict(
                    l=20,
                    r=20,
                    t=40,
                    b=40
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    except:

        st.info(
            "Data grafik tidak tersedia."
        )

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.image(
    logo,
    use_container_width=True
)

st.sidebar.markdown(
    "## Eco-Forest Valuation"
)

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
        label="🌳 Profil Hutan",
        value=len(profil_hutan)
    )

    c2.metric(
        label="🪵 Produksi",
        value=len(produksi_kayu)
    )

    c3.metric(
        label="📊 Master Data",
        value=len(master_data)
    )

    c4.metric(
        label="📈 Dashboard",
        value=len(dashboard)
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

    st.title(
        "🌳 Profil Hutan KPH Cepu"
    )

    st.dataframe(
        profil_hutan,
        use_container_width=True,
        hide_index=True,
        height=420
    )

    create_chart_from_table(
        profil_hutan,
        "Variable",
        "Value",
        "Grafik Profil Hutan"
    )

# =====================================================
# PRODUKSI KAYU
# =====================================================

elif menu == "Produksi Kayu":

    st.title(
        "🪵 Produksi Kayu"
    )

    st.dataframe(
        produksi_kayu,
        use_container_width=True,
        hide_index=True,
        height=420
    )

    create_chart_from_table(
        produksi_kayu,
        "Variabel",
        "Nilai",
        "Grafik Produksi Kayu"
    )

# =====================================================
# MASTER DATA
# =====================================================

elif menu == "Master Data":

    st.title(
        "📊 Master Data"
    )

    st.info(
        "Master data merupakan basis data yang digunakan dalam analisis ekonomi sumber daya hutan."
    )

    st.dataframe(
        master_data,
        use_container_width=True,
        hide_index=True,
        height=420
    )

    create_chart_from_table(
        master_data,
        "Variable",
        "Value",
        "Grafik Master Data"
    )

# =====================================================
# PARAMETER SIMULASI
# =====================================================

elif menu == "Parameter Simulasi":

    st.title(
        "⚙️ Parameter Simulasi"
    )

    st.dataframe(
        parameter,
        use_container_width=True,
        hide_index=True,
        height=420
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

    st.title(
        "📈 Dashboard Summary"
    )

    st.dataframe(
        dashboard,
        use_container_width=True,
        hide_index=True,
        height=420
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
