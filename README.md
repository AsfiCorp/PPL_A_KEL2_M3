# Araya Business Hub - Modul 3: Manajemen Partner

Repositori resmi Modul 3 (Manajemen Partner) Araya Business Hub untuk seluruh tim (Frontend, Backend, Database, QA/Tester, dan Analis/Desain). Modul backend dan REST API terintegrasi langsung di dalam proyek ini.

## Integrasi Antarmodul
- **M1 (Akun & Auth)**: Integrasi akun mitra, autentikasi JWT, dan password hashing write-only.
- **M2 (Master Usaha)**: Relasi `unit_usaha_id` untuk kategori dan klasifikasi unit usaha mitra.
- **M4 (Penjualan & Produk)**: Validasi prasyarat status partner terverifikasi sebelum penambahan produk/jasa.
- **M5 (Katalog Publik)**: Penyediaan daftar partner terverifikasi (Kontrak K-06).

## Arsitektur Branch
- `main`: Production release.
- `test`: Staging dan integrasi tim bersama.
- `feature/<id-task>-<nama>`: Branch pengerjaan fitur.

**Aturan Kerja Git:**
1. Pengerjaan selalu di branch `feature/*`.
2. Selesai pengerjaan, buat Pull Request ke branch `test`.
3. Dilarang push langsung ke branch `main` atau `test`.

## Quick Start
1. Clone repositori:
```bash
git clone git@github.com:AsfiCorp/PPL_A_KEL2_M3.git
cd PPL_A_KEL2_M3
```

2. Setup otomatis (membuat venv, instal dependensi, migrasi basis data, dan menjalankan automated test):
```bash
./setup.sh
```

3. Jalankan server lokal:
```bash
./venv/bin/python manage.py runserver
```
Server aktif di `http://127.0.0.1:8000/`.

## Dokumentasi API & Kontrak Antarmodul

Sesuai standar Araya Business Hub, dokumentasi teknis API Modul 3 tidak diletakkan secara verbose di `README.md`, melainkan dikelola secara terpusat pada berkas spesifikasi resmi:

1. **OpenAPI 3.0 Specification**:
   - Berkas Skema: [`docs/openapi.yaml`](docs/openapi.yaml)
   - Endpoint Skema: `http://127.0.0.1:8000/api/m3/v1/openapi.yaml`

2. **Dokumentasi Interaktif (Swagger UI)**:
   - Akses via browser: `http://127.0.0.1:8000/api/m3/v1/docs/`

3. **Paket Resmi Dokumentasi API & Koleksi Postman**:
   - Seluruh dokumen kontrak teknis dan koleksi pengujian resmi tersimpan di direktori **`flow/docs/`**:
     - **01. Ringkasan Integrasi & Panduan Cepat (PDF)**: `flow/docs/01_Ringkasan_Integrasi_M3_README.pdf` (Cheat sheet orientasi cepat integrasi lintas modul, konfigurasi koneksi, ringkasan endpoint, dan aturan validasi).
     - **02. Kontrak API & Event Resmi (PDF)**: `flow/docs/02_API_Contract_Modul_3.pdf` (Spesifikasi teknis lengkap mencakup konvensi, autentikasi JWT/Service-Key, parameter multipart dokumen KTP & selfie, validasi NIK 16 digit, password kuat, kode publik `PRT-YYYYMMDD-XXXX`, status mapping, dan katalog kode galat).
     - **03. OpenAPI Specification (YAML)**: `flow/docs/03_openapi_modul3.yaml` (Kontrak mesin standar OpenAPI 3.0.3).
     - **04. Matriks Event & Hubungan Antarmodul (PDF)**: `flow/docs/04_Matriks_Event_&_Hubungan_Antarmodul.pdf` (Rincian ketergantungan lintas modul K-06, K-01, M2-Ref, M4-Prereq, spesifikasi event pub/sub, matriks transisi status, diagram sequence end-to-end, dan checklist integrasi).
     - **05. Postman Collection v2.1.0 (JSON)**: `flow/docs/05_Postman_Collection_M3.json` (Koleksi siap pakai untuk pengujian registrasi, dual lookup ID/PRT, validasi 422/409, dan katalog K-06).

## Ringkasan Endpoint Utama Modul 3

| Method | Endpoint | Keterangan & Kontrak |
| :--- | :--- | :--- |
| `POST` | `/api/m3/v1/partners/` | Registrasi mandiri calon partner (M3-US1, T4.2, T5.2). Mendukung multipart unggah Foto KTP & Selfie KTP, NIK 16 digit, password kuat, auto-generate `partner_id` (`PRT-YYYYMMDD-XXXX`), status awal `pending`. |
| `GET` | `/api/m3/v1/partners/{id}/` | Detail & pelacakan status partner (M3-US3, T10, T11). Mendukung **Dual Lookup** via ID numerik maupun string `partner_id`. Menampilkan `rejection_reason` hanya jika status `ditolak`. |
| `GET` | `/api/m3/v1/partners/?status=terverifikasi` | Katalog partner terverifikasi untuk konsumsi Modul 5 dan Modul 4 (**Kontrak K-06**) dengan pagination (`page`, `per_page`) dan pencarian (`q`). |
| `GET` | `/api/m3/v1/docs/` | Antarmuka interaktif Swagger UI. |
| `GET` | `/api/m3/v1/openapi.yaml` | Kontrak skema OpenAPI 3.0.3 YAML. |

## Antarmuka Django (UI)
- Beranda: `/`
- Toko Saya: `/toko-saya/`
- Formulir Pendaftaran Partner: `/pendaftaran-partner/`
- Status Pengajuan Partner: `/pendaftaran-partner/status/`

## Pengujian Otomatis (Automated Tests)
Jalankan pengujian menggunakan script resmi:
```bash
./run_test.sh
```
Atau via Django runner:
```bash
./venv/bin/python manage.py test partners -v 2
```
Seluruh 36 test suite (unit tests dan QA acceptance tests) berjalan otomatis dengan status lulus 100%.
