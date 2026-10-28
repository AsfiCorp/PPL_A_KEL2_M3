# Araya Business Hub - Modul 3: Manajemen Partner

Repositori bersama Modul 3 (Manajemen Partner) Araya Business Hub untuk seluruh tim (Frontend, Backend, Database, dan QA/Tester). Modul backend dan API DRF terintegrasi langsung di dalam proyek ini.

## Integrasi Modul
- M1: Akun dan autentikasi
- M2: Kategori unit usaha
- M4: Input produk/jasa partner terverifikasi
- M5: Katalog publik partner

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

## API Pendaftaran Partner (POST)
- Endpoint: `/api/partners/register/`
- Method: `POST`
- Content-Type: `application/json` atau `multipart/form-data`

### Request Body
| Field | Tipe | Wajib | Keterangan |
| :--- | :--- | :--- | :--- |
| `nama_usaha` | String | Ya | Nama toko/usaha |
| `kategori_usaha` | String | Ya | "Produk" atau "Jasa" |
| `deskripsi_usaha` | String | Ya | Deskripsi usaha |
| `alamat_usaha` | String | Ya | Alamat usaha |
| `nomor_telepon_usaha` | String | Ya | Nomor telepon/WhatsApp |
| `email_usaha` | String | Ya | Email usaha (unik) |
| `profil_usaha` | File (Gambar) | Tidak | File PNG, JPG, atau SVG |

### Contoh Response (201 Created)
```json
{
  "status": "success",
  "message": "Pendaftaran partner berhasil dikirim dan menunggu verifikasi.",
  "data": {
    "id": 1,
    "nama_usaha": "Toko Berkah",
    "kategori_usaha": "Produk",
    "deskripsi_usaha": "Menjual sembako",
    "alamat_usaha": "Jl. Gatot Subroto No. 45",
    "nomor_telepon_usaha": "081234567890",
    "email_usaha": "berkah@example.com",
    "profil_usaha": null,
    "status": "pending",
    "created_at": "2026-10-28T15:34:00Z"
  }
}
```

### Contoh Integrasi Frontend
```javascript
const formData = new FormData();
formData.append('nama_usaha', 'Toko Berkah');
formData.append('kategori_usaha', 'Produk');
formData.append('deskripsi_usaha', 'Menjual sembako');
formData.append('alamat_usaha', 'Jl. Merdeka No. 1');
formData.append('nomor_telepon_usaha', '081234567890');
formData.append('email_usaha', 'berkah@example.com');

fetch('http://127.0.0.1:8000/api/partners/register/', {
  method: 'POST',
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Pengujian (Tester)
Jalankan test:
```bash
./run_test.sh
```
Atau:
```bash
./venv/bin/python manage.py test partners -v 2
```
