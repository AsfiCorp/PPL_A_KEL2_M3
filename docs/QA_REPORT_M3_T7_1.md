# Laporan QA & Hasil Pengujian Fungsional Modul 3 (M3-US1 & M3-US3)

**Tanggal Pengujian:** 11 November 2026  
**Peran:** Quality Assurance (QA Engineer)  
**Lingkup Pengujian:** 
- `PRO-29` (Task T7): Pengujian Fungsional Acceptance Criteria M3-US1
- `PRO-226` (Task T7.1): Automated Testing Registrasi Berkas Dokumen (Foto KTP & Selfie KTP) dan Akun Aplikasi
- Validasi Kontrak K-06, Status Tracking M3-US3 (Task T10), dan Proteksi `rejection_reason` (Task T11)

---

## 1. Ringkasan Eksekusi Pengujian Otomatis

- **Total Test Cases:** 41 Tests
- **Status:** 41 Passed, 0 Failed, 0 Errors (**100% Lulus**)
- **Test Runner Waktu Eksekusi:** ~1.16 detik
- **Database:** SQLite In-Memory Test Database

---

## 2. Matriks Pengujian Fungsional & Acceptance Criteria

| ID Test | Kriteria Pengujian / Skenario | Hasil Aktual | Status |
|---|---|---|---|
| **AC-01** | Registrasi form lengkap JSON & Multipart -> respons `201 Created` + status `pending` | HTTP 201, `success: true`, status `pending` tercatat di DB | **PASSED** |
| **AC-02** | Isian form tidak lengkap -> penolakan `422/400` beserta rincian field error | HTTP 422, `error.fields` memuat field yang hilang | **PASSED** |
| **AC-03** | Email usaha duplikat -> penolakan `409 Conflict` dengan kode `EMAIL_DUPLICATE` | HTTP 409, pesan menyatakan email telah terdaftar | **PASSED** |
| **AC-04** | Format email tidak valid -> penolakan `422 Unprocessable Entity` (`EMAIL_INVALID`) | HTTP 422, pesan format email tidak valid | **PASSED** |
| **AC-05** | Kategori usaha di luar `Produk` / `Jasa` | HTTP 422, penolakan pada field `kategori_usaha` | **PASSED** |
| **T7.1-01** | Registrasi multipart dengan dokumen Foto KTP (PNG/JPG) & Foto Selfie KTP | HTTP 201, berkas tersimpan di media folder, path tersimpan di DB | **PASSED** |
| **T7.1-02** | Format berkas bukan gambar (misal .txt) pada upload dokumen KTP | HTTP 422, pesan `Format berkas harus berupa gambar JPG atau PNG.` | **PASSED** |
| **T7.1-03** | Berkas dokumen melebihi batas 5 MB | HTTP 422, pesan `Ukuran berkas maksimal 5 MB.` | **PASSED** |
| **T7.1-04** | Validasi NIK tepat 16 digit numerik | HTTP 201 untuk 16 digit; HTTP 422 jika < 16 digit atau mengandung alfabet | **PASSED** |
| **T7.1-05** | Validasi Password kuat (>= 8 karakter & kombinasi huruf + angka) | HTTP 201 untuk password kuat; HTTP 422 untuk < 8 karakter / alfabet murni / numerik murni | **PASSED** |
| **T7.1-06** | Keamanan Kredensial: Password ter-hash dengan algoritma aman (bcrypt/pbkdf2) | Password disimpan di kolom `password_hash`, tidak pernah muncul di respons JSON | **PASSED** |
| **T7.1-07** | Auto-generate unik `partner_id` format `PRT-YYYYMMDD-XXXX` | Partner ID terbentuk otomatis dan tercantum pada data respons | **PASSED** |
| **T10-01** | GET status pendaftaran berdasarkan ID / Partner ID | HTTP 200 dengan data lengkap; HTTP 404 jika tidak ditemukan | **PASSED** |
| **T11-01** | Proteksi `rejection_reason` / `alasan_penolakan` | Bernilai `null` jika status `pending`/`terverifikasi`; hanya terisi jika status `ditolak` | **PASSED** |

---

## 3. Kesimpulan & Rekomendasi QA
Seluruh implementasi backend dari tim pengembang telah memenuhi kriteria kontrak API bersama dan Acceptance Criteria produk. Fitur siap diintegrasikan ke lingkungan pengujian (`test`).
