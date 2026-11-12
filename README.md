# Araya Business Hub - Modul 3: Manajemen Partner

Repositori resmi Modul 3 (Manajemen Partner) Araya Business Hub untuk seluruh tim (Frontend, Backend, Database, QA/Tester, dan Analis/Desain). Modul ini bertindak sebagai **Single Source of Truth** untuk pendaftaran mandiri pelaku usaha, verifikasi identitas penanggung jawab, pengelolaan akun mitra, dan penyediaan master data partner terverifikasi untuk platform bersama.

---

## 1. Arsitektur & Aliran Integrasi Lintas Modul

Modul 3 terhubung langsung dengan empat modul lain dalam ekosistem Araya Business Hub:

```
                      +-----------------------------+
                      |   MODUL 2: UNIT USAHA       |
                      |   - Master Kategori Usaha   |
                      |   - Dashboard Agregasi UMKM |
                      +-----------------------------+
                                     |
               (GET Master Kategori) | (Metrik Agregat Mitra)
                                     v
+-------------------+      +-----------------------+      +---------------------+
|    CALON MITRA    | ===> |        MODUL 3        | ===> |  MODUL 5: KATALOG   |
| (Frontend Web M3) | <=== |  (MANAJEMEN PARTNER)  |      |  - Katalog Publik   |
+-------------------+      |  - Registrasi Mitra   |      |  - Etalase Toko K-06|
                           |  - Legalitas & NIK    |      +---------------------+
+-------------------+      |  - Keputusan Status   |
|   ADMINISTRATOR   | ---> |  - Dual Lookup ID/PRT |      +---------------------+
| (Verifikasi KTP)  |      +-----------------------+ ===> | MODUL 4: PENJUALAN  |
+-------------------+            |           ^            | - Izin Posting Prod |
                                 |           |            | - Otorisasi Jual    |
             (Sync Akun Mitra)   |           | (Bearer    +---------------------+
             saat Terverifikasi  v           |  JWT Auth)
                      +-----------------------------+
                      |    MODUL 1: USER & AUTH     |
                      |    - Autentikasi Pengguna   |
                      |    - Penerbitan Token JWT   |
                      +-----------------------------+
```

### Rincian Integrasi per Modul:

1. **Modul 1 (User & Autentikasi - Kontrak K-01)**:
   - **Penerimaan Kredensial**: Calon mitra mendaftarkan `email_usaha` dan `password` pada formulir Modul 3. Backend Modul 3 memvalidasi ketat (minimal 8 karakter kombinasi huruf dan angka), mengenkripsinya secara aman menggunakan `make_password()` (PBKDF2 SHA-256) secara *write-only*, dan tidak pernah membocorkannya pada respons API.
   - **Sinkronisasi Akun saat Approval**: Ketika Admin menyetujui pendaftaran mitra (status berubah menjadi `terverifikasi`), Modul 3 menyinkronkan data akun mitra ke Modul 1 via endpoint internal untuk mengaktifkan akun dan menerima `user_id`.
   - **Autentikasi JWT**: Mitra melakukan login di portal Modul 1 dan memperoleh token JWT bertanda tangan dengan klaim `{ user_id, email, role: "partner", partner_id }`. Modul 3 memverifikasi token ini melalui header `Authorization: Bearer <token>` pada endpoint privat.

2. **Modul 2 (Master Unit Usaha & Dashboard Agregasi - Kontrak M2-Ref)**:
   - **Inbound Dropdown Kategori**: Formulir pendaftaran mitra di Frontend/Backend Modul 3 memanggil endpoint Modul 2 (`GET /api/m2/v1/unit-usaha/`) untuk mempopulasikan pilihan kategori bisnis ke dropdown formulir secara dinamis. Nilai yang dipilih disimpan pada kolom `unit_usaha_id`.
   - **Graceful Fallback**: Jika layanan Modul 2 sedang luring atau belum siap di lingkungan lokal, sistem Modul 3 menerapkan fallback aman ke kategori default (`Produk` dan `Jasa`) sehingga registrasi tidak terhenti.
   - **Outbound Dashboard Agregasi**: Dashboard eksekutif Modul 2 memanggil Modul 3 (`GET /api/m3/v1/partners/?status=terverifikasi&unit_usaha_id={id}`) untuk menampilkan ringkasan jumlah dan sebaran mitra UMKM yang aktif.

3. **Modul 4 (Penjualan & Produk - Kontrak K-06 / M4-Prereq)**:
   - **Otorisasi Tambah Produk/Jasa**: Sebelum mitra diperbolehkan mengunggah katalog produk atau jasa di Modul 4, backend Modul 4 memanggil `GET /api/m3/v1/partners/{id}/` untuk memeriksa status legalitas partner.
   - **Aturan Akses**: Hanya partner berstatus `terverifikasi` yang diberikan izin input produk/jasa. Mitra berstatus `pending`, `ditolak`, atau `ditangguhkan` otomatis ditolak oleh Modul 4.

4. **Modul 5 (Katalog Publik & Website - Kontrak K-06)**:
   - **Penyedia Etalase Resmi**: Modul 5 mengonsumsi data etalase toko mitra aktif melalui endpoint `GET /api/m3/v1/partners/?status=terverifikasi`.
   - **Fitur Konsumsi**: Endpoint mendukung parameter pagination (`page`, `per_page`) serta filter pencarian nama atau lokasi (`q`) sehingga dapat memuat banyak mitra secara cepat dan efisien.

---

## 2. Diagram Alur Komunikasi Antarmodul (Sequence Flow)

```
Calon Mitra      Modul 2 (Master)    Modul 3 (Backend)    Admin (Review)     Modul 1 (Auth)     Modul 5 (Katalog)   Modul 4 (Sales)
    |                    |                    |                 |                  |                   |                  |
    |-- 1. Buka Form --->|                    |                 |                  |                   |                  |
    |   Registrasi       |<- 2. GET Unit Usaha|                 |                  |                   |                  |
    |                    |-- 3. Daftar Kategori                 |                  |                   |                  |
    |-- 4. Submit Data & Berkas Foto -------->|                 |                  |                   |                  |
    |   (KTP, Selfie, Password, NIK)          |-- 5. Validasi & Hashing            |                   |                  |
    |                                         |-- 6. Generate PRT Code             |                   |                  |
    |<- 7. 201 Created {partner_id: PRT-...}-|-- 8. Status: 'pending'              |                   |                  |
    |                                         |                 |                  |                   |                  |
    |-- 9. Pantau Status (GET PRT Code) ----->|                 |                  |                   |                  |
    |<- 10. 200 OK {status: 'pending'} -------|                 |                  |                   |                  |
    |                                         |                 |<-- 11. Review ---|                   |                  |
    |                                         |                 |    KTP & Selfie  |                   |                  |
    |                                         |<-- 12. Keputusan: 'terverifikasi' -|                   |                  |
    |                                         |-- 13. Sync Akun Mitra ------------>|                   |                  |
    |                                         |<- 14. 201 User Created (user_id)---|                   |                  |
    |                                         |                                                        |                  |
    |                                         |<- 15. GET /partners/?status=terverifikasi (K-06)-------|                  |
    |                                         |-- 16. 200 OK { data: [mitra_terverifikasi] } ---------->|                  |
    |                                         |                                                                           |
    |                                         |<- 17. GET /partners/{id}/ (Cek Status Hak Jual Mitra)---------------------|
    |                                         |-- 18. 200 OK { status: 'terverifikasi' } --------------------------------->|
    |                                         |                                                       (Mitra boleh input  |
    |                                         |                                                        produk di Modul 4) |
```

---

## 3. Siklus Hidup Status Partner & Dampak Antarmodul

| Status Partner | Hak Akses Modul 1 (Auth) | Hak Akses Modul 4 (Jual) | Tampilan Modul 5 (Katalog) | Logika Status & Tampilan Antarmuka |
| :--- | :--- | :--- | :--- | :--- |
| `pending` | Akun belum aktif | Dilarang input produk | Belum tampil di etalase | Menunggu verifikasi admin; tombol formulir pendaftaran terkunci. |
| `terverifikasi` | Akun aktif, login diizinkan | Otorisasi dibuka penuh | Tampil otomatis di katalog | Mitra disetujui; tombol antarmuka mengarahkan ke login Modul 1. |
| `ditolak` | Akun ditolak | Dilarang transaksi | Tidak tampil di katalog | Menampilkan alasan penolakan (`rejection_reason`) persisten (Task T11); tombol daftar ulang terbuka untuk perbaikan berkas. |
| `ditangguhkan` | Sesi login dibekukan | Produk di-*freeze* | Toko disembunyikan | Akun dibekukan sementara karena pelanggaran; menampilkan kontak bantuan. |

---

## 4. Ringkasan Endpoint Utama Modul 3

Seluruh endpoint beralamat dasar `/api/m3/v1/` dan mengembalikan respons beramplop standar (`success`, `status`, `message`, `data`, `error`):

| Method | Endpoint | Hak Akses | Keterangan & Kontrak |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/m3/v1/partners/` | Publik | Pendaftaran mandiri calon partner (M3-US1). Menerima multipart unggahan foto KTP & selfie KTP, NIK tepat 16 digit, password minimal 8 karakter kombinasi, auto-generate kode publik `partner_id` (`PRT-YYYYMMDD-XXXX`), status awal `pending`. |
| `GET` | `/api/m3/v1/partners/{id}/` | Publik / Partner / Admin | Detail & pelacakan status partner (M3-US3). Mendukung **Dual Lookup** via ID numerik maupun kode string `PRT-...`. Menampilkan field `rejection_reason` hanya jika status `ditolak` (Task T11). |
| `GET` | `/api/m3/v1/partners/?status=terverifikasi` | Publik / Modul 5 / Modul 4 | Katalog partner terverifikasi (**Kontrak K-06**) dengan pagination (`page`, `per_page`) dan filter pencarian nama/kota (`q`). |
| `GET` | `/api/m3/v1/docs/` | Semua Tim | Dokumentasi interaktif Swagger UI untuk pengujian API langsung via peramban web. |
| `GET` | `/api/m3/v1/openapi.yaml` | Semua Tim | Spesifikasi kontrak OpenAPI 3.0.3 YAML standar mesin. |

---

## 5. Arsitektur Branch & Aturan Kerja Git

- `main`: Branch rilis produksi.
- `test`: Branch staging dan integrasi pengujian tim bersama.
- `feature/<id-task>-<nama>`: Branch pengerjaan fitur individual.

**Aturan Kerja Git:**
1. Seluruh pengerjaan wajib dilakukan pada branch `feature/*`.
2. Setelah pengerjaan selesai dan pengujian lulus, buat Pull Request (PR) ke branch `test`.
3. Dilarang melakukan push langsung ke branch `main` atau `test`.

---

## 6. Quick Start

### 1. Klon Repositori:
```bash
git clone git@github.com:AsfiCorp/PPL_A_KEL2_M3.git
cd PPL_A_KEL2_M3
```

### 2. Setup Otomatis:
Menyiapkan virtual environment, menginstal dependensi, migrasi basis data, dan menjalankan pengujian otomatis:
```bash
./setup.sh
```

### 3. Menjalankan Server Lokal:
```bash
./venv/bin/python manage.py runserver
```
Server aktif di `http://127.0.0.1:8000/`.

---

## 7. Antarmuka Django (UI)

- Beranda: `/`
- Toko Saya: `/toko-saya/`
- Formulir Pendaftaran Partner: `/pendaftaran-partner/`
- Status Pengajuan Partner: `/pendaftaran-partner/status/`

---
Form UI mengirim `multipart/form-data` ke `/api/partners/register/`, menampilkan error validasi dari API, lalu membuka halaman status setelah menerima respons sukses. Gambar PNG, JPG, atau JPEG hingga 5 MB didukung. Pastikan JavaScript browser aktif untuk mengirim form melalui API.

## 8. Pengujian Otomatis (Automated Tests)

Jalankan pengujian menggunakan skrip resmi:
```bash
./run_test.sh
```
Atau via Django runner:
```bash
./venv/bin/python manage.py test partners -v 2
```
Seluruh 36 test suite (unit tests dan QA acceptance tests) berjalan otomatis dengan status kelulusan 100%.
