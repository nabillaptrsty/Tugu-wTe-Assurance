# Dashboard Pemantauan — Tugu WtE Assurance Bridge

Dashboard Streamlit (tema ungu) untuk menampilkan pemantauan risiko, data
Smart Waste Sorting, dan proyeksi keuangan solusi **Tugu WtE Assurance Bridge**
kepada kreditur & investor.

## Isi Folder
```
tugu-wte-dashboard/
├── app.py                     # aplikasi utama Streamlit
├── requirements.txt           # daftar library yang dibutuhkan
├── .streamlit/
│   └── config.toml            # tema warna ungu
└── README.md
```

## Alur Membuat & Deploy (dari Nol)

### 1. Coba jalankan dulu di komputer sendiri (opsional tapi disarankan)
```bash
pip install -r requirements.txt
streamlit run app.py
```
Browser otomatis terbuka di `http://localhost:8501`. Cek dulu semua tab
(Ringkasan, Risk Mapping, Parametric Monitoring, Roadmap) sebelum lanjut deploy.

### 2. Buat repository baru di GitHub
1. Login ke github.com → klik **New repository**.
2. Beri nama, misalnya `tugu-wte-dashboard`.
3. Pilih **Public** (Streamlit Community Cloud gratis butuh repo public,
   kecuali kamu pakai akun berbayar).
4. Jangan centang "Add README" (karena sudah ada di folder ini) — atau centang
   saja lalu nanti tinggal timpa.

### 3. Push folder ini ke GitHub
Jalankan di dalam folder `tugu-wte-dashboard`:
```bash
git init
git add .
git commit -m "Dashboard Tugu WtE Assurance Bridge - versi awal"
git branch -M main
git remote add origin https://github.com/USERNAME/tugu-wte-dashboard.git
git push -u origin main
```
Ganti `USERNAME` dengan username GitHub kamu.

### 4. Deploy ke Streamlit Community Cloud
1. Buka https://share.streamlit.io lalu login pakai akun GitHub.
2. Klik **New app**.
3. Pilih repository `tugu-wte-dashboard`, branch `main`.
4. Isi **Main file path** dengan `app.py`.
5. Klik **Deploy** — tunggu proses build (biasanya 1–3 menit).
6. Setelah selesai, kamu dapat link publik, contoh:
   `https://tugu-wte-dashboard.streamlit.app` — ini yang dilampirkan di
   pitch deck / dipresentasikan ke juri.

### 5. Update dashboard di kemudian hari
Setiap kali mengubah `app.py` atau file lain:
```bash
git add .
git commit -m "update dashboard"
git push
```
Streamlit Community Cloud otomatis re-deploy setiap ada push baru ke branch
yang terhubung — tidak perlu setting ulang.

## Mengganti Data Contoh dengan Data Asli
Semua data di `app.py` saat ini masih **contoh/ilustratif** (di dalam fungsi
`load_risk_mapping`, `load_financial_projection`, `load_feedstock_monitoring`,
`load_roadmap`). Untuk versi lanjutan:
- Ganti isi `DataFrame` dengan data hasil riset tim, atau
- Baca dari file `.csv`/`.xlsx` (`pd.read_csv("data/feedstock.csv")`), atau
- Sambungkan ke API Smart Waste Sorting jika sudah tersedia endpoint-nya.

## Kustomisasi Warna
Tema ungu diatur di dua tempat:
- `.streamlit/config.toml` → warna bawaan komponen Streamlit.
- Bagian `st.markdown(""" <style> ... """)` di awal `app.py` → styling
  tambahan untuk kartu metrik dan sidebar.

Ganti kode warna hex (`#7C3AED`, `#4C1D95`, dst.) sesuai kebutuhan branding.
