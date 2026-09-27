"""
Dashboard Pemantauan Tugu WtE Assurance Bridge
Untuk Kreditur & Investor - Business Case Competition IDEANATION 2026
Tim: Indah Tri Maharani, Nurfidah Nabilla Putriasty, Primadhani Syah Putera
Universitas Gunadarma
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Tugu WtE Assurance Bridge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS TAMBAHAN — nuansa ungu konsisten di seluruh komponen
# ============================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #FBF7FF; }
    div[data-testid="stMetric"] {
        background-color: #F3E8FF;
        border: 1px solid #C4B5FD;
        border-radius: 12px;
        padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] { color: #5B21B6; font-weight: 600; }
    div[data-testid="stMetricValue"] { color: #4C1D95; }
    h1, h2, h3 { color: #4C1D95; }
    section[data-testid="stSidebar"] { background-color: #2E1065; }
    section[data-testid="stSidebar"] * { color: #EDE9FE !important; }
    .badge-hijau {background-color:#DCFCE7;color:#166534;padding:3px 10px;border-radius:8px;font-size:13px;}
    .badge-kuning {background-color:#FEF9C3;color:#854D0E;padding:3px 10px;border-radius:8px;font-size:13px;}
    .badge-merah {background-color:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:8px;font-size:13px;}
    </style>
    """,
    unsafe_allow_html=True,
)

PURPLE_SCALE = ["#EDE9FE", "#C4B5FD", "#A78BFA", "#8B5CF6", "#7C3AED", "#5B21B6", "#4C1D95"]

# ============================================================
# DATA CONTOH (ganti dengan data riil / koneksi API saat sudah ada)
# ============================================================

@st.cache_data
def load_risk_mapping():
    return pd.DataFrame({
        "Tahap Siklus Proyek": [
            "Pengumpulan & Transportasi Sampah",
            "Pembangunan Fasilitas (Konstruksi)",
            "Operasi Pembangkit",
            "Distribusi Listrik",
            "Carbon Credit",
            "Lintas Tahap (Cyber/SCADA-IoT)",
        ],
        "Risiko Utama": [
            "Ketidakpastian volume/komposisi feedstock, keterlambatan pasokan",
            "Keterlambatan konstruksi, kerusakan alat berat, cuaca ekstrem",
            "Kerusakan mesin/boiler, kebakaran, risiko lingkungan",
            "Kegagalan interkoneksi jaringan, gagal bayar offtaker",
            "Kegagalan validasi/verifikasi kredit karbon",
            "Serangan siber pada sistem SCADA/IoT",
        ],
        "Produk Asuransi": [
            "Parametric Waste-Supply Cover; Inland Transit Cover",
            "Contractor's All Risk (CAR); Delay in Start-Up (DSU)",
            "Machinery Breakdown; Business Interruption; Environmental Liability",
            "Revenue-Linked Business Interruption",
            "Wrap-Around Policy (perluasan cakupan karbon)",
            "Cyber Risk Insurance (polis payung)",
        ],
        "Status Cakupan": ["Aktif", "Aktif", "Aktif", "Dalam Kajian", "Dalam Kajian", "Aktif"],
    })


@st.cache_data
def load_financial_projection():
    return pd.DataFrame({
        "Tahun": ["Tahun 1", "Tahun 2", "Tahun 3"],
        "Fokus Tahap": ["Pilot & Bukti Konsep", "Standardisasi & Kolaborasi", "Ekspansi Nasional"],
        "Jumlah Proyek Kumulatif": [2, 6, 12],
        "Premi Bruto Min (Rp Miliar)": [3, 15, 30],
        "Premi Bruto Max (Rp Miliar)": [8, 25, 45],
        "Loss Ratio Min (%)": [35, 40, 40],
        "Loss Ratio Max (%)": [40, 45, 45],
    })


@st.cache_data
def load_feedstock_monitoring():
    # Simulasi data harian dari Smart Waste Sorting selama 30 hari terakhir
    dates = pd.date_range(end=datetime.today(), periods=30)
    import numpy as np
    rng = np.random.default_rng(42)
    volume = 180 + rng.normal(0, 12, size=30).cumsum() * 0.15 + rng.normal(0, 8, size=30)
    volume = volume.clip(min=110)
    kalori = 1650 + rng.normal(0, 25, size=30)
    return pd.DataFrame({
        "Tanggal": dates,
        "Volume Sampah (ton/hari)": volume.round(1),
        "Nilai Kalori (kcal/kg)": kalori.round(0),
    })


@st.cache_data
def load_roadmap():
    return pd.DataFrame({
        "Tahap": ["Tahap I — Pilot", "Tahap II — Standardisasi & Kolaborasi", "Tahap III — Ekspansi Nasional"],
        "Progress (%)": [70, 25, 5],
        "Deskripsi": [
            "Kemitraan 1–2 proyek PSEL prioritas; integrasi data Smart Waste Sorting ke risk assessment",
            "Pengolahan data pilot menjadi standar asesmen risiko; perluasan kolaborasi mitra",
            "Replikasi solusi secara nasional; penyelarasan regulasi WtE, taksonomi OJK, agenda ESG",
        ],
    })


risk_df = load_risk_mapping()
fin_df = load_financial_projection()
feed_df = load_feedstock_monitoring()
roadmap_df = load_roadmap()

VOLUME_THRESHOLD = 150  # ton/hari — ambang batas kontrak Parametric Waste-Supply Cover

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚡ Tugu WtE\nAssurance Bridge")
    st.caption("Dashboard Pemantauan untuk Kreditur & Investor")
    st.divider()
    proyek_pilihan = st.selectbox(
        "Pilih Proyek PSEL",
        ["Proyek Pilot A", "Proyek Pilot B", "Gabungan Semua Proyek"],
    )
    tahun_pilihan = st.select_slider(
        "Tahun Proyeksi", options=["Tahun 1", "Tahun 2", "Tahun 3"], value="Tahun 1"
    )
    st.divider()
    st.caption("Terakhir diperbarui: " + datetime.today().strftime("%d %B %Y"))
    st.caption("Sumber data: Smart Waste Sorting API · Underwriting Engine Tugu")

st.title("⚡ Dashboard Pemantauan — Tugu WtE Assurance Bridge")
st.caption(f"Menampilkan data untuk: **{proyek_pilihan}**")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Ringkasan", "🗺️ Risk Mapping Siklus Proyek", "📡 Parametric Monitoring", "🚀 Roadmap & Proyeksi Keuangan"]
)

# ---------------- TAB 1: RINGKASAN ----------------
with tab1:
    row = fin_df[fin_df["Tahun"] == tahun_pilihan].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah Proyek Kumulatif", f"{row['Jumlah Proyek Kumulatif']} proyek")
    c2.metric(
        "Estimasi Premi Bruto/Tahun",
        f"Rp {row['Premi Bruto Min (Rp Miliar)']}–{row['Premi Bruto Max (Rp Miliar)']} M",
    )
    c3.metric(
        "Asumsi Loss Ratio",
        f"{row['Loss Ratio Min (%)']}–{row['Loss Ratio Max (%)']}%",
    )
    volume_terkini = feed_df["Volume Sampah (ton/hari)"].iloc[-1]
    status = "Di Atas Ambang ✅" if volume_terkini >= VOLUME_THRESHOLD else "Di Bawah Ambang ⚠️"
    c4.metric("Status Feedstock Terkini", status, f"{volume_terkini:.0f} ton/hari")

    st.divider()
    col_a, col_b = st.columns([1.3, 1])

    with col_a:
        st.subheader("Cakupan Wrap-Around Policy Terintegrasi")
        komponen = pd.DataFrame({
            "Komponen": [
                "Contractor's All Risk", "Delay in Start-Up", "Machinery Breakdown",
                "Environmental Liability", "Cyber Risk", "Revenue-Linked BI",
            ],
            "Status": ["Aktif", "Aktif", "Aktif", "Aktif", "Aktif", "Dalam Kajian"],
        })
        fig = px.bar(
            komponen, x="Komponen", y=[1] * len(komponen), color="Status",
            color_discrete_map={"Aktif": "#7C3AED", "Dalam Kajian": "#DDD6FE"},
        )
        fig.update_layout(showlegend=True, yaxis_visible=False, xaxis_title="", height=320,
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Tahapan Implementasi")
        for _, r in roadmap_df.iterrows():
            st.markdown(f"**{r['Tahap']}**")
            st.progress(int(r["Progress (%)"]))
        st.caption("Progress bersifat ilustratif untuk keperluan studi kasus.")

# ---------------- TAB 2: RISK MAPPING ----------------
with tab2:
    st.subheader("Peta Risiko Sepanjang Siklus Hidup Proyek WtE")
    st.dataframe(
        risk_df.style.map(
            lambda v: "background-color:#DCFCE7" if v == "Aktif" else "background-color:#FEF9C3",
            subset=["Status Cakupan"],
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("#### Ilustrasi Cakupan per Tahap")
    fig2 = px.timeline(
        pd.DataFrame({
            "Tahap": risk_df["Tahap Siklus Proyek"],
            "Mulai": pd.date_range("2026-01-01", periods=6, freq="60D"),
            "Selesai": pd.date_range("2026-03-01", periods=6, freq="60D"),
        }),
        x_start="Mulai", x_end="Selesai", y="Tahap",
        color="Tahap", color_discrete_sequence=PURPLE_SCALE,
    )
    fig2.update_layout(showlegend=False, height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- TAB 3: PARAMETRIC MONITORING ----------------
with tab3:
    st.subheader("Pemantauan Data Smart Waste Sorting (Parametric Waste-Supply Cover)")
    st.caption("Kompensasi otomatis terpicu apabila volume harian berada di bawah ambang kontrak.")

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=feed_df["Tanggal"], y=feed_df["Volume Sampah (ton/hari)"],
        mode="lines+markers", name="Volume Aktual", line=dict(color="#7C3AED", width=3),
    ))
    fig3.add_hline(y=VOLUME_THRESHOLD, line_dash="dash", line_color="#DC2626",
                    annotation_text="Ambang Kontrak (150 ton/hari)", annotation_position="top left")
    fig3.update_layout(height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        yaxis_title="ton/hari", xaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        fig4 = px.area(
            feed_df, x="Tanggal", y="Nilai Kalori (kcal/kg)",
            color_discrete_sequence=["#A78BFA"],
        )
        fig4.update_layout(height=300, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            title="Tren Nilai Kalori Feedstock")
        st.plotly_chart(fig4, use_container_width=True)
    with col_d:
        hari_dibawah_ambang = int((feed_df["Volume Sampah (ton/hari)"] < VOLUME_THRESHOLD).sum())
        st.metric("Hari di Bawah Ambang (30 hari terakhir)", f"{hari_dibawah_ambang} hari")
        st.metric("Rata-rata Volume 30 Hari", f"{feed_df['Volume Sampah (ton/hari)'].mean():.1f} ton/hari")
        if hari_dibawah_ambang > 5:
            st.warning("Frekuensi di bawah ambang cukup tinggi — pertimbangkan index-based repricing.")
        else:
            st.success("Pasokan feedstock relatif stabil terhadap ambang kontrak.")

# ---------------- TAB 4: ROADMAP & PROYEKSI KEUANGAN ----------------
with tab4:
    st.subheader("Proyeksi Keuangan Tiga Tahun (Ilustratif)")
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=fin_df["Tahun"], y=fin_df["Premi Bruto Max (Rp Miliar)"],
        name="Premi Bruto Maks (Rp M)", marker_color="#C4B5FD",
    ))
    fig5.add_trace(go.Bar(
        x=fin_df["Tahun"], y=fin_df["Premi Bruto Min (Rp Miliar)"],
        name="Premi Bruto Min (Rp M)", marker_color="#7C3AED",
    ))
    fig5.add_trace(go.Scatter(
        x=fin_df["Tahun"], y=fin_df["Loss Ratio Max (%)"],
        name="Loss Ratio Maks (%)", yaxis="y2", mode="lines+markers", line=dict(color="#4C1D95"),
    ))
    fig5.update_layout(
        barmode="group", height=400,
        yaxis=dict(title="Premi Bruto (Rp Miliar)"),
        yaxis2=dict(title="Loss Ratio (%)", overlaying="y", side="right"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.dataframe(fin_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Tahapan Implementasi")
    for _, r in roadmap_df.iterrows():
        with st.expander(f"{r['Tahap']} — {r['Progress (%)']}% berjalan"):
            st.write(r["Deskripsi"])
            st.progress(int(r["Progress (%)"]))

st.divider()
st.caption(
    "Dashboard ini dibuat untuk keperluan studi kasus Business Case Competition "
    "IDEANATION 2026 (SB-IPB x Tugu Insurance) — Tim Universitas Gunadarma. "
    "Seluruh data bersifat ilustratif."
)
