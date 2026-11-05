# Araya Business Hub - Modul 3: Manajemen Partner

Repositori bersama Modul 3 (Manajemen Partner) Araya Business Hub untuk seluruh tim (Frontend, Backend, Database, dan QA/Tester). Modul backend dan API DRF terintegrasi langsung di dalam proyek ini.

## Integrasi Modul
- M1: Akun dan autentikasi
- M2: Kategori unit usaha
- M4: Input produk/jasa partner terverifikasi
- M5: Katalog publik partner (Kontrak K-06)

## Arsitektur Branch
- `main`: Production release
- `test`: Staging dan integrasi tim
- `feature/<id-task>-<nama>`: Branch pengerjaan fitur

Aturan:
1. Pengerjaan selalu di branch `feature/*`.
2. Selesai pengerjaan, buat Pull Request ke branch `test`.
3. Dilarang push langsung ke `main` atau `test`.

## Quick Start
Clone repo:
```bash
git clone git@github.com:AsfiCorp/PPL_A_KEL2_M3.git
cd PPL_A_KEL2_M3
```

Setup otomatis (venv, install dependencies, migrate, dan test):
```bash
./setup.sh
```

Jalankan server:
```bash
./venv/bin/python manage.py runserver
```
Server berjalan di `http://127.0.0.1:8000/`.

## Dokumentasi OpenAPI dan Swagger
Dokumentasi interaktif Swagger UI dan kontrak OpenAPI v1:
- Halaman Dokumentasi API: `http://127.0.0.1:8000/api/m3/v1/docs/`
- Berkas OpenAPI Schema: `http://127.0.0.1:8000/api/m3/v1/openapi.yaml` atau berkas `docs/openapi.yaml`

## Antarmuka Django (UI)
Antarmuka pendaftaran partner menggunakan template Django:
- Beranda: `/`
- Toko saya: `/toko-saya/`
- Form pendaftaran partner: `/pendaftaran-partner/`
- Status pengajuan: `/pendaftaran-partner/status/`

## API Endpoints Modul 3 (Sesuai Panduan API Bersama)

### 1. Pendaftaran Partner Baru (POST)
- Endpoint: `/api/m3/v1/partners/` (alias kompatibilitas: `/api/partners/register/`)
- Method: `POST`
- Content-Type: `application/json` atau `multipart/form-data`

#### Request Body
| Field | Tipe | Wajib | Keterangan |
| :--- | :--- | :--- | :--- |
| `nama_usaha` | String | Ya | Nama toko/usaha |
| `kategori_usaha` | String | Ya | "Produk" atau "Jasa" |
| `deskripsi_usaha` | String | Ya | Deskripsi usaha |
| `alamat_usaha` | String | Ya | Alamat usaha |
| `nomor_telepon_usaha` | String | Ya | Nomor telepon/WhatsApp |
| `email_usaha` | String | Ya | Email usaha (unik) |
| `profil_usaha` | File (Gambar) | Tidak | File PNG, JPG, atau JPEG |

#### Response Sukses (201 Created)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": null,
    "nama_usaha": "Toko Berkah",
    "kategori_usaha": "Produk",
    "deskripsi_usaha": "Menjual sembako",
    "alamat_usaha": "Jl. Gatot Subroto No. 45",
    "nomor_telepon_usaha": "081234567890",
    "email_usaha": "berkah@example.com",
    "profil_usaha": null,
    "status": "pending",
    "alasan_penolakan": null,
    "alasan_penangguhan": null,
    "created_at": "2026-10-28T15:34:00Z"
  }
}
```

#### Response Galat Validasi (422 Unprocessable Entity)
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Isian tidak lolos validasi. Periksa kelengkapan data.",
    "fields": {
      "nama_usaha": "Nama usaha wajib diisi."
    }
  }
}
```

#### Response Galat Duplikasi Email (409 Conflict)
```json
{
  "success": false,
  "error": {
    "code": "EMAIL_DUPLICATE",
    "message": "Email sudah terdaftar.",
    "fields": {
      "email_usaha": "Email sudah terdaftar."
    }
  }
}
```

### 2. Daftar Partner Terverifikasi untuk Katalog M5 (GET / K-06)
- Endpoint: `/api/m3/v1/partners/?status=terverifikasi`
- Method: `GET`

### 3. Detail dan Status Pendaftaran Partner (GET / M3-US3)
- Endpoint: `/api/m3/v1/partners/{id}/`
- Method: `GET`

## Pengujian (Tester)
Jalankan test:
```bash
./run_test.sh
```
Atau:
```bash
./venv/bin/python manage.py test partners -v 2
```
