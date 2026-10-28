# Araya Business Hub - Modul 3: Manajemen Partner

Backend service untuk pendaftaran dan verifikasi partner.

## Quick Start
Jalankan script setup:
```bash
./setup.sh
```
Jalankan server:
```bash
./venv/bin/python manage.py runserver
```
Server berjalan di `http://127.0.0.1:8000/`.

## Testing
Jalankan test:
```bash
./run_test.sh
```

## API Endpoint Pendaftaran Partner
- URL: `POST /api/partners/register/`
- Content-Type: `application/json` atau `multipart/form-data`

### Request Body
- `nama_usaha` (string, wajib)
- `kategori_usaha` (string, wajib: `Produk` | `Jasa`)
- `deskripsi_usaha` (string, wajib)
- `alamat_usaha` (string, wajib)
- `nomor_telepon_usaha` (string, wajib)
- `email_usaha` (string email, wajib, unik)
- `profil_usaha` (file gambar, opsional)

### Response Sukses (201 Created)
```json
{
  "status": "success",
  "message": "Pendaftaran partner berhasil dikirim dan menunggu verifikasi.",
  "data": {
    "id": 1,
    "nama_usaha": "Toko Berkah",
    "kategori_usaha": "Produk",
    "deskripsi_usaha": "Deskripsi usaha",
    "alamat_usaha": "Alamat usaha",
    "nomor_telepon_usaha": "081234567890",
    "email_usaha": "toko@example.com",
    "profil_usaha": null,
    "status": "pending",
    "created_at": "2026-10-28T15:30:00Z"
  }
}
```

## Branch Strategy
- `main`: Rilis stabil.
- `test`: Integrasi dan testing tim.
- `feature/*`: Pengerjaan task. Merge ke `test` via Pull Request.
