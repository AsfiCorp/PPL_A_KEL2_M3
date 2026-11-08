# Araya Business Hub - Modul 3: Manajemen Partner

Repositori resmi Modul 3 (Manajemen Partner) Araya Business Hub untuk seluruh tim (Frontend, Backend, Database, QA/Tester, dan Analis/Desain). Modul backend dan REST API terintegrasi langsung di dalam proyek ini.

## Integrasi Antarmodul

Modul 3 bertindak sebagai **Single Source of Truth** untuk pendaftaran dan verifikasi legalitas mitra usaha:

```
[M2: Unit Usaha]       --> (GET Master Kategori)    --> [M3: Registrasi & Verifikasi]
[M1: User & Auth]      <-- (Sync Akun Terverifikasi) <-- [M3: Manajemen Partner]
[M1: User & Auth]      --> (Bearer JWT Auth)        --> [M3: Endpoint Terproteksi]
[M3: Master Partner]   --> (Kontrak K-06 Katalog)   --> [M5: Katalog Publik]
[M3: Status Partner]   --> (Otorisasi Hak Jual)     --> [M4: Penjualan / Produk]
```

- **M1 (Akun & Auth - Kontrak K-01)**: Menerima kredensial mitra, mengenkripsi password dengan `make_password()` (PBKDF2 SHA-256) secara *write-only*, menyinkronkan akun saat verifikasi admin disetujui, dan memvalidasi otentikasi via token JWT (`role: partner`).
- **M2 (Master Usaha - Kontrak M2-Ref)**: Menyediakan data kategori usaha untuk dropdown formulir registrasi mitra (`unit_usaha_id`), dengan mekanisme *graceful fallback* jika Modul 2 luring. Dashboard Modul 2 memanggil metrik agregat partner aktif dari Modul 3.
- **M4 (Penjualan & Produk - Kontrak K-06 / M4-Prereq)**: Memvalidasi prasyarat status partner (`terverifikasi`) via `GET /api/m3/v1/partners/{id}/` sebelum memperbolehkan mitra memposting produk/jasa.
- **M5 (Katalog Publik - Kontrak K-06)**: Menyajikan daftar etalase toko mitra aktif via `GET /api/m3/v1/partners/?status=terverifikasi` dengan pagination dan pencarian `q`.

---

## Siklus Hidup Status Partner & Dampak Antarmodul

| Status | Hak Akses Modul 1 (Auth) | Hak Akses Modul 4 (Jual) | Tampilan Modul 5 (Katalog) | Logika Status & Tampilan UI |
| :--- | :--- | :--- | :--- | :--- |
| `pending` | Akun belum aktif | Dilarang input produk | Belum tampil di etalase | Menunggu verifikasi admin; tombol form terkunci. |
| `terverifikasi` | Akun aktif, login diizinkan | Otorisasi dibuka penuh | Tampil otomatis di katalog | Memicu event `partner.verified`, tombol diarahkan ke login M1. |
| `ditolak` | Akun ditolak | Dilarang transaksi | Tidak tampil | Menampilkan `rejection_reason` persisten (T11); tombol daftar ulang aktif. |
| `ditangguhkan` | Sesi login dibekukan | Produk di-*freeze* | Toko disembunyikan sementara | Pelanggaran toko; menampilkan kontak bantuan admin. |

---

## 7 Tahap Penyatuan Lintas Modul (Unification Roadmap)

1. **Tahap 1 (Environment & Secrets)**: Penyeragaman konfigurasi `.env` (`M1_BASE_URL`, `M2_BASE_URL`, `M4_BASE_URL`, `M5_BASE_URL`, `X_SERVICE_KEY`, `JWT_SECRET`).
2. **Tahap 2 (Inbound Modul 2)**: Integrasi dropdown unit usaha via `GET /api/m2/v1/unit-usaha/` dengan fallback aman.
3. **Tahap 3 (Inbound Modul 1)**: Sinkronisasi akun saat persetujuan admin dan implementasi middleware verifikasi Bearer JWT Token.
4. **Tahap 4 (Outbound Modul 4)**: Penyediaan endpoint validasi status hak posting produk (`GET /api/m3/v1/partners/{id}/`).
5. **Tahap 5 (Outbound Modul 5)**: Penyediaan API katalog toko mitra terverifikasi (**Kontrak K-06**).
6. **Tahap 6 (Event Bus / Asinkron)**: Penerbitan event `partner.registered` dan `partner.verified` berformat amplop standar dan idempoten.
7. **Tahap 7 (Pengujian Bersama)**: Eksekusi pengujian integrasi end-to-end menggunakan Postman Collection pada shared staging server.

---

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

---

## Ringkasan Endpoint Utama Modul 3

| Method | Endpoint | Hak Akses | Keterangan & Kontrak |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/m3/v1/partners/` | Publik | Registrasi mandiri calon partner (M3-US1, T4.2, T5.2). Menerima multipart foto KTP & selfie KTP, NIK 16 digit, password kuat, auto-generate `partner_id` (`PRT-YYYYMMDD-XXXX`), status awal `pending`. |
| `GET` | `/api/m3/v1/partners/{id}/` | Publik / Partner / Admin | Detail & pelacakan status partner (M3-US3, T10, T11). Mendukung **Dual Lookup** via ID numerik maupun kode `PRT-...`. Menampilkan `rejection_reason` hanya jika status `ditolak`. |
| `GET` | `/api/m3/v1/partners/?status=terverifikasi` | Publik / Modul 5 / Modul 4 | Katalog partner terverifikasi (**Kontrak K-06**) dengan pagination (`page`, `per_page`) dan filter pencarian nama/kota (`q`). |
| `GET` | `/api/m3/v1/docs/` | Semua Tim | Antarmuka dokumentasi interaktif Swagger UI. |
| `GET` | `/api/m3/v1/openapi.yaml` | Semua Tim | Kontrak spesifikasi skema OpenAPI 3.0.3 YAML. |

---

## Dokumentasi Lengkap & Koleksi Postman

Dokumentasi teknis lengkap dan mendalam tersedia di folder **`flow/docs/`**:

- **[01_Ringkasan_Integrasi_M3_README.pdf](flow/docs/01_Ringkasan_Integrasi_M3_README.pdf)**: Panduan cepat integrasi, response envelope, aturan validasi, dan alur status.
- **[02_API_Contract_Modul_3.pdf](flow/docs/02_API_Contract_Modul_3.pdf)**: Kontrak API resmi, validasi multipart form-data, DFD Level 0 & 1, detail teknis koneksi M1 & M2, dan katalog kode error standar.
- **[03_openapi_modul3.yaml](flow/docs/03_openapi_modul3.yaml)**: Kontrak OpenAPI 3.0.3 standar mesin untuk Swagger UI dan code generation.
- **[04_Matriks_Event_&_Hubungan_Antarmodul.pdf](flow/docs/04_Matriks_Event_&_Hubungan_Antarmodul.pdf)**: Matriks ketergantungan lintas modul (K-06, K-01, M2-Ref), DFD, diagram siklus hidup status, alur sequence komunikasi, spesifikasi event pub/sub, dan integration checklist.
- **[05_Postman_Collection_M3.json](flow/docs/05_Postman_Collection_M3.json)**: Koleksi Postman siap pakai mencakup skenario pendaftaran sukses, dual lookup, validasi error, dan katalog K-06.

---

## Antarmuka Django (UI)
- Beranda: `/`
- Toko Saya: `/toko-saya/`
- Formulir Pendaftaran Partner: `/pendaftaran-partner/`
- Status Pengajuan Partner: `/pendaftaran-partner/status/`

---

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
