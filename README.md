# Araya Business Hub - Modul 3: Manajemen Partner

Repositori resmi Modul 3 (Manajemen Partner) Araya Business Hub untuk seluruh peran tim (Frontend, Backend, Database, QA/Tester, dan System Analyst). Modul ini bertindak sebagai **Single Source of Truth** untuk pendaftaran mandiri pelaku usaha, verifikasi identitas dan legalitas penanggung jawab, sinkronisasi akun mitra, dan penyediaan master data partner terverifikasi untuk ekosistem platform bersama.

Dokumentasi ini mencakup ruang lingkup menyeluruh (**Sprint 1** dan **Sprint 2**), lengkap dengan pembagian tanggung jawab, kontrak antarmodul, dan alur teknis integrasi.

---

## 1. Roadmap & Ruang Lingkup per Sprint

Pengembangan Modul 3 dibagi secara tegas ke dalam dua sprint utama:

### [SPRINT 1] Fondasi Pendaftaran & Pelacakan Status Mitra
* **M3-US1 (Pendaftaran Partner)**: Pendaftaran mandiri oleh calon mitra usaha (pengisian data profil usaha, berkas foto KTP & selfie KTP, NIK 16 digit, kredensial akun, otomatis membuat kode publik `partner_id`, status awal `pending`).
* **M3-US3 (Status Pendaftaran)**: Pelacakan status verifikasi pendaftaran terkini secara mandiri oleh mitra (`pending`, `terverifikasi`, atau `ditolak` beserta alasan penolakan `rejection_reason`).
* **Integrasi Inbound Modul 2**: Pengambilan data master unit usaha untuk pilihan kategori di formulir pendaftaran (`GET /api/m2/v1/unit-usaha/`) beserta mekanisme graceful fallback.
* **Integrasi Outbound Modul 5**: Penyediaan katalog partner terverifikasi untuk etalase publik (**Kontrak K-06**).

### [SPRINT 2] Verifikasi Legalitas, Tata Kelola Akun & Ekosistem Penjualan
* **M3-US2 (Verifikasi Pendaftaran oleh Administrator)**: Pemeriksaan berkas legalitas pendaftaran oleh Admin, aksi persetujuan (approval) atau penolakan dengan alasan wajib.
* **M3-US4 (Penangguhan & Pengaktifan Kembali Partner)**: Fitur pembekuan (suspend) partner bermasalah dengan alasan wajib, serta re-aktivasi partner yang telah memenuhi syarat.
* **Integrasi Outbound Modul 1 (User & Auth)**:
  * Autentikasi Admin via Bearer JWT Token (`role: "admin"`).
  * Sinkronisasi akun otomatis secara *machine-to-machine* saat partner disetujui (kirim `name`, `email`, `password`, `role: "partner"`, `unit_usaha_id`, dan `partner_id`), serta pencatatan `user_id` balasan dari Modul 1.
* **Integrasi Inbound Modul 4 (Penjualan & Produk)**: Pengecekan izin operasional mitra sebelum diizinkan mengunggah produk atau jasa (hanya mitra `terverifikasi` yang diizinkan).
* **Integrasi Outbound Modul 2 (Dashboard Eksekutif)**: Penyediaan metrik agregasi partner terverifikasi per kategori bisnis untuk dashboard pimpinan.

---

## 2. Tabel User Story & Acceptance Criteria Resmi

| Sprint | Kode US | User Story | Acceptance Criteria (Lengkap) |
| :--- | :--- | :--- | :--- |
| **[SPRINT 1]** | **M3-US1** | Sebagai Partner, saya ingin mendaftar ke platform, supaya bisa memasarkan produk/jasa saya. | 1. Given partner isi form pendaftaran lengkap, When submit, Then status "Pending".<br/>2. Given partner isi form tidak lengkap, When submit, Then sistem tolak & tampilkan field yang kurang.<br/>3. Given email sudah terdaftar, When submit, Then sistem menolak pendaftaran dan menampilkan pesan "Email sudah terdaftar".<br/>4. Given format email tidak valid, When submit, Then sistem menolak pendaftaran dan menampilkan pesan "Format email tidak valid". |
| **[SPRINT 1]** | **M3-US3** | Sebagai Partner, saya ingin melihat status pendaftaran saya, supaya tahu perkembangan verifikasi. | 1. Given partner sudah submit pendaftaran, When membuka halaman status, Then status terkini (pending/terverifikasi/ditolak) tampil.<br/>2. Given pendaftaran ditolak, When partner membuka halaman status, Then alasan penolakan tampil. |
| **[SPRINT 2]** | **M3-US2** | Sebagai Administrator, saya ingin memverifikasi (menyetujui/menolak) pendaftaran Partner, supaya hanya partner terverifikasi yang tampil di platform. | 1. Given status pending, When admin setujui, Then status "terverifikasi" & tampil di platform.<br/>2. Given status pending, When admin tolak, Then status "ditolak" + alasan tercatat.<br/>3. Given terdapat data Partner yang terdaftar, When halaman verifikasi dibuka, Then sistem menampilkan daftar Partner beserta status pendaftarannya.<br/>4. Given alasan penolakan belum diisi, When penolakan dikonfirmasi, Then sistem menolak proses dan meminta alasan penolakan. |
| **[SPRINT 2]** | **M3-US4** | Sebagai Administrator, saya ingin menangguhkan dan mengaktifkan kembali Partner, supaya partner bermasalah tidak tampil di platform. | 1. Given partner terverifikasi, When admin tangguhkan + isi alasan, Then partner tidak tampil di platform & alasan tercatat.<br/>2. Given partner ditangguhkan, When admin aktifkan kembali, Then partner kembali tampil di platform.<br/>3. Given Partner berstatus "terverifikasi", When halaman pengelolaan Partner dibuka, Then sistem menampilkan daftar Partner yang terverifikasi.<br/>4. Given alasan penangguhan belum diisi, When penangguhan dikonfirmasi, Then sistem menolak proses dan meminta alasan penangguhan. |

---

## 3. Arsitektur Komunikasi Antarmodul

```
                      +---------------------------------------+
                      |       MODUL 2: UNIT USAHA             |
                      | [SPRINT 1] Master Kategori Dropdown   |
                      | [SPRINT 2] Dashboard Agregasi UMKM    |
                      +---------------------------------------+
                                          |
        [SPRINT 1] (GET Master Kategori)  |  [SPRINT 2] (Metrik Agregat Mitra)
                                          v
+-----------------------+     +-------------------------------+     +-----------------------+
|  CALON / AKTIF MITRA  | ===>|            MODUL 3            |===> | MODUL 5: KATALOG      |
| [SPRINT 1] Registrasi | <===|      (MANAJEMEN PARTNER)      |     | [SPRINT 1] Etalase    |
| [SPRINT 1] Cek Status |     | - Kode Publik: partner_id     |     |   Toko Publik (K-06)  |
+-----------------------+     | - Legalitas KTP & NIK         |     +-----------------------+
                              | - Status Approval & Suspend   |
+-----------------------+     +-------------------------------+     +-----------------------+
|     ADMINISTRATOR     | --->        |               ^             | MODUL 4: PENJUALAN    |
| [SPRINT 2] Verifikasi |             |               |             | [SPRINT 2] Otorisasi  |
| [SPRINT 2] Penangguhan|             |               |             |   Hak Jual Produk     |
+-----------------------+  [SPRINT 2] |    [SPRINT 2] |             +-----------------------+
                         (Sinkronisasi|   (Bearer JWT |
                            Akun)     v      Auth)    |
                      +---------------------------------------+
                      |         MODUL 1: USER & AUTH          |
                      | - Pintu Gerbang Login Terpusat        |
                      | - Pembuatan Akun & Hash Password      |
                      | - Penerbitan Token JWT                |
                      +---------------------------------------+
```

### Rincian Keterkaitan Antarmodul:

#### 1. Keterkaitan dengan Modul 1 (User & Autentikasi - SSO)
* **[SPRINT 1] Isolasi Akun Pending**: Selama fase pendaftaran di Sprint 1, kredensial calon mitra ditampung sementara di Modul 3 dengan status `pending`. Akun belum didaftarkan ke Modul 1 agar database Modul 1 bersih dari pendaftar fiktif/spam.
* **[SPRINT 2] Sinkronisasi Otomatis saat Disetujui**: Begitu Admin Modul 3 menyetujui pendaftaran mitra, backend Modul 3 otomatis memanggil API Modul 1 (`POST /api/m1/v1/users`) lewat jalur aman HTTPS (*server-to-server*) dengan payload:
  * `name`: Nama penanggung jawab
  * `email`: Email partner
  * `password`: Password pendaftaran
  * `role`: `"partner"`
  * `unit_usaha_id`: ID unit usaha
  * `partner_id`: Kode registrasi Modul 3 (misal: `"PRT-20261109-A1B2"`)
* **[SPRINT 2] Penyimpanan Relasi Dua Arah**: Modul 1 membalas dengan `user_id` (misal: `42`). Modul 3 menyimpan `user_id` ini ke database partner. Saat mitra login melalui portal Modul 1, token JWT yang diterbitkan membawa klaim `user_id` dan `partner_id`.
* **[SPRINT 2] Autentikasi Akses Admin**: Administrator login melalui Modul 1, lalu token JWT ber-role `"admin"` dikirimkan via header `Authorization: Bearer <token>` untuk membuka halaman verifikasi dan mengeksekusi persetujuan di Modul 3.

#### 2. Keterkaitan dengan Modul 2 (Master Unit Usaha & Dashboard Eksekutif)
* **[SPRINT 1] Dropdown Kategori Usaha**: Halaman pendaftaran mitra memanggil `GET /api/m2/v1/unit-usaha/` untuk memuat opsi kategori unit usaha secara dinamis. Hasil pilihan mitra disimpan pada kolom `unit_usaha_id`.
* **[SPRINT 1] Graceful Fallback**: Jika server Modul 2 sedang offline, sistem Modul 3 otomatis menggunakan kategori standar bawaan (`Produk` dan `Jasa`) tanpa mengganggu proses pendaftaran.
* **[SPRINT 2] Dashboard Agregasi Eksekutif**: Modul 2 memanggil endpoint agregasi Modul 3 (`GET /api/m3/v1/partners/?status=terverifikasi&unit_usaha_id={id}`) untuk menampilkan grafik dan sebaran mitra UMKM aktif.

#### 3. Keterkaitan dengan Modul 4 (Penjualan, Produk & Jasa)
* **[SPRINT 2] Otorisasi Hak Jual**: Sebelum mitra dapat menambah produk atau jasa di Modul 4, backend Modul 4 memvalidasi legalitas mitra dengan memanggil `GET /api/m3/v1/partners/{id}/`.
* **[SPRINT 2] Aturan Status**: Hanya mitra berstatus `terverifikasi` yang diizinkan mengunggah produk. Mitra berstatus `pending`, `ditolak`, atau `ditangguhkan` otomatis diblokir dari transaksi penjualan.

#### 4. Keterkaitan dengan Modul 5 (Katalog Publik & Etalase Web)
* **[SPRINT 1] Sumber Data Etalase Resmi (Kontrak K-06)**: Modul 5 mengonsumsi data mitra aktif melalui endpoint publik `GET /api/m3/v1/partners/?status=terverifikasi`.
* **[SPRINT 1 & 2] Filter & Pagination**: Endpoint mendukung parameter `page`, `per_page`, dan filter pencarian nama/kota `q`. Mitra yang berstatus `ditolak` atau `ditangguhkan` otomatis disaring dan tidak akan muncul di katalog publik.

---

## 4. Diagram Alur Terpadu (Sequence Flow)

```
Calon / Mitra       Modul 2 (Master)      Modul 3 (Backend)      Admin M3           Modul 1 (Auth)       Modul 5 (Katalog)     Modul 4 (Penjualan)
      |                    |                      |                  |                     |                    |                     |
===================================================== [ SPRINT 1 : PENDAFTARAN & STATUS ] =====================================================
      |-- 1. Buka Form --->|                      |                  |                     |                    |                     |
      |   Pendaftaran      |<- 2. GET Unit Usaha--|                  |                     |                    |                     |
      |                    |-- 3. List Kategori ->|                  |                     |                    |                     |
      |-- 4. Submit Form & Berkas -------------->|                  |                     |                    |                     |
      |   (KTP, Selfie, Password, NIK, Usaha)     |-- 5. Validasi Dokumen                  |                    |                     |
      |                                           |-- 6. Generate PRT-...                  |                    |                     |
      |<- 7. 201 Created {partner_id: PRT-...}----|-- 8. Status: 'pending'                 |                    |                     |
      |                                           |                  |                     |                    |                     |
      |-- 9. Cek Status (GET {partner_id}) ------>|                  |                     |                    |                     |
      |<- 10. 200 OK {status: 'pending'} ---------|                  |                     |                    |                     |
      |                                           |                                                             |                     |
      |                                           |<- 11. GET /partners/?status=terverifikasi (K-06)------------|                     |
      |                                           |-- 12. 200 OK (Hanya toko terverifikasi yang tampil)-------->|                     |
      |                                           |                  |                     |                    |                     |
===================================================== [ SPRINT 2 : VERIFIKASI & TATA KELOLA ] =================================================
      |                                           |                  |<-- 13. Login M1 ----|                    |                     |
      |                                           |                  |-- 14. Token JWT --->|                    |                     |
      |                                           |                  |    (Role: admin)    |                    |                     |
      |                                           |                  |                     |                    |                     |
      |                                           |<- 15. Buka List Partner (Bearer JWT)---|                    |                     |
      |                                           |-- 16. Data Partner & Berkas KTP ------>|                    |                     |
      |                                           |                  |                     |                    |                     |
      |                                           |                  |-- 17. Review Berkas |                    |                     |
      |                                           |                  |                     |                    |                     |
      |  [SKENARIO ACC / DISETUJUI]               |                  |                     |                    |                     |
      |                                           |<- 18. Klik "Setujui" (ACC) ------------|                    |                     |
      |                                           |-- 19. POST /api/m1/v1/users (Server-to-Server)------------->|                     |
      |                                           |   (name, email, password, role: partner, partner_id)        |                     |
      |                                           |<- 20. 201 Created {user_id: 42} ----------------------------|                     |
      |                                           |-- 21. Simpan user_id & Ubah Status: 'terverifikasi'         |                     |
      |                                           |                                                             |                     |
      |  [SKENARIO LOGIN PARTNER]                 |                                                             |                     |
      |-- 22. Login di Portal Modul 1 ----------------------------------------------------->|                     |                     |
      |<- 23. 200 OK + JWT Token {user_id: 42, partner_id: PRT-...} ------------------------|                     |                     |
      |                                           |                                                             |                     |
      |  [SKENARIO OTORISASI JUAL MODUL 4]        |                                                             |                     |
      |-- 24. Tambah Produk Baru ---------------------------------------------------------------------------------------------------->|
      |                                           |<- 25. GET /partners/{id}/ (Cek Status Legalitas Mitra)----------------------------|
      |                                           |-- 26. 200 OK {status: 'terverifikasi'} -------------------------------------------->|
      |<- 27. Produk Berhasil Diunggah ------------------------------------------------------------------------------------------------|
      |                                           |                  |                     |                    |                     |
      |  [SKENARIO SUSPEND / PENANGGUHAN]         |                  |                     |                    |                     |
      |                                           |<- 28. Klik "Tangguhkan" + Alasan ------|                    |                     |
      |                                           |-- 29. Status: 'ditangguhkan'           |                    |                     |
      |                                           |   (Otomatis disembunyikan dari Modul 4 & Modul 5)           |                     |
```

---

## 5. Matriks Siklus Hidup Status Partner

| Status Partner | Modul 1 (Akun Login) | Modul 4 (Hak Jual) | Modul 5 (Katalog Publik) | Logika Bisnis & Penanganan Sistem |
| :--- | :--- | :--- | :--- | :--- |
| **`pending`** *(Sprint 1)* | Belum dibuat di Modul 1 | Ditolak mengunggah produk | Belum ditampilkan di katalog | Menunggu verifikasi berkas oleh admin. Mitra memantau status secara mandiri. |
| **`terverifikasi`** *(Sprint 2)* | Akun aktif di Modul 1 | Otorisasi buka penuh | Ditampilkan resmi di katalog | Dokumen lolos kurasi. Modul 3 menyinkronkan data akun ke Modul 1. |
| **`ditolak`** *(Sprint 2)* | Tidak dibuat di Modul 1 | Ditolak bertransaksi | Tidak ditampilkan di katalog | Dokumen tidak valid. Field `rejection_reason` tampil pada halaman status mitra untuk perbaikan berkas. |
| **`ditangguhkan`** *(Sprint 2)* | Akses dibekukan | Produk di-*freeze* | Toko disembunyikan | Mitra melanggar aturan. Admin wajib menyertakan alasan penangguhan. |

---

## 6. Ringkasan Endpoint API Lengkap

Semua endpoint memiliki prefix dasar `/api/m3/v1/` dan mengembalikan format respons beramplop standar (`success`, `data`, `error`).

| Sprint | Method | Endpoint | Hak Akses | Keterangan & Kontrak |
| :--- | :--- | :--- | :--- | :--- |
| **[SPRINT 1]** | `POST` | `/api/m3/v1/partners/` | Publik | Pendaftaran mandiri calon mitra (M3-US1). Menerima multipart dokumen (foto KTP, selfie KTP, profil), NIK 16 digit, data usaha, kredensial password. Menghasilkan kode publik `partner_id` (`PRT-YYYYMMDD-XXXX`), status awal otomatis `pending`. |
| **[SPRINT 1]** | `GET` | `/api/m3/v1/partners/{id}/` | Publik / Mitra | Detail & pelacakan status mitra (M3-US3). Mendukung **Dual Lookup** (ID numerik internal atau string `partner_id`). Menampilkan `rejection_reason` jika status `ditolak`. |
| **[SPRINT 1]** | `GET` | `/api/m3/v1/partners/?status=terverifikasi` | Publik / M5 | Etalase resmi katalog mitra aktif (**Kontrak K-06**) dengan dukungan pagination (`page`, `per_page`) dan filter pencarian (`q`). |
| **[SPRINT 2]** | `GET` | `/api/m3/v1/admin/partners/` | Admin (JWT M1) | Menampilkan daftar seluruh mitra yang mendaftar beserta status verifikasinya (M3-US2 AC 3). Dilindungi autentikasi Bearer JWT `role: "admin"`. |
| **[SPRINT 2]** | `POST` | `/api/m3/v1/admin/partners/{id}/verify/` | Admin (JWT M1) | Eksekusi persetujuan atau penolakan pendaftaran (M3-US2). Jika setujui, panggil API Modul 1 untuk membuat akun. Jika tolak, wajib menyertakan `alasan_penolakan`. |
| **[SPRINT 2]** | `POST` | `/api/m3/v1/admin/partners/{id}/suspend/` | Admin (JWT M1) | Penangguhan mitra terverifikasi (M3-US4 AC 1 & 4). Wajib menyertakan alasan penangguhan. Menyembunyikan toko dari platform. |
| **[SPRINT 2]** | `POST` | `/api/m3/v1/admin/partners/{id}/reactivate/` | Admin (JWT M1) | Mengaktifkan kembali mitra yang ditangguhkan (M3-US4 AC 2). Mengembalikan toko ke etalase platform. |

---

## 7. Rute Antarmuka Web (Frontend)

| Sprint | Rute Web | Tipe Pengguna | Deskripsi Halaman |
| :--- | :--- | :--- | :--- |
| **[SPRINT 1]** | `/pendaftaran-partner/` | Calon Mitra | Formulir pendaftaran mitra mandiri lengkap dengan unggah berkas KTP dan pemilihan unit usaha. |
| **[SPRINT 1]** | `/pendaftaran-partner/status/` | Calon Mitra | Halaman mandiri untuk melacak status verifikasi menggunakan kode unik `partner_id`. |
| **[SPRINT 2]** | `/admin/login/` | Administrator | Pintu masuk login admin terintegrasi dengan API login Modul 1. |
| **[SPRINT 2]** | `/admin/verifikasi-partner/` | Administrator | Dashboard admin untuk meninjau berkas pendaftaran partner serta aksi Setujui / Tolak (M3-US2). |
| **[SPRINT 2]** | `/admin/kelola-partner/` | Administrator | Halaman pengelolaan partner terverifikasi untuk penangguhan dan pengaktifan kembali (M3-US4). |

---

## 8. Panduan Menjalankan & Deployment

### Menjalankan di Lingkungan Lokal:
```bash
# 1. Klon repositori
git clone -b test https://github.com/AsfiCorp/PPL_A_KEL2_M3.git
cd PPL_A_KEL2_M3

# 2. Setup otomatis dependensi dan migrasi basis data
./setup.sh

# 3. Jalankan automated test
./run_test.sh

# 4. Jalankan development server
./venv/bin/python manage.py runserver
```

### Opsi Deployment Cloud (Gratis Rp 0):
1. **Frontend Web & Dokumentasi API (Scalar Docs)**: Di-deploy ke **Vercel** gratis.
2. **Backend API Django (Modul 3)**:
   * **Opsi PythonAnywhere**: Sangat ramah Django, mendukung database SQLite dan folder berkas `media/` secara langsung.
   * **Opsi Vercel Serverless**: Menggunakan koneksi database cloud gratis (**Neon.tech / Supabase**) dan media storage gratis (**Cloudinary**).
