# Araya Business Hub — Modul 3: Manajemen Partner
> **Mata Kuliah**: Proyek Perangkat Lunak (Capstone Project) — IF21W0705  
> **Kelas / Kelompok**: Kelas A / Kelompok 2 (Modul 3 - A3)  
> **Platform**: Araya Business Hub  

Repository ini berisi implementasi backend untuk **Modul 3: Manajemen Partner**, yang bertanggung jawab atas seluruh siklus hidup kemitraan (*partner lifecycle*), mulai dari registrasi mandiri calon Partner hingga proses verifikasi dan pengelolaan status oleh Administrator.

---

## 📌 Peta Keterhubungan Modul
Modul 3 beroperasi terintegrasi dengan modul-modul lain di Kelas A Fondasi:
* **M1 (Kel. A1)**: Akun pengguna dasar, autentikasi, hak akses divisi, dan audit log terpusat.
* **M2 (Kel. A2)**: Master kategori unit usaha yang dipilih partner saat registrasi.
* **M4 (Kel. A4)**: Input produk/jasa oleh Partner yang telah berstatus *Terverifikasi*.
* **M5 (Kel. A5)**: Katalog publik platform yang menampilkan produk/jasa Partner aktif.

---

## 🌿 Arsitektur Branch Git & Standar CI/CD

### 1. Struktur Branch
Repository ini menerapkan strategi branching berbasis **Git-Flow / Feature-Branch**:

```text
main (Production / Stable Release untuk evaluasi dosen)
  │
  └── test (Staging / Integrasi tim: Backend, Frontend, Tester, Database)
        │
        ├── feature/PRO-26-T4-api-post-pendaftaran
        ├── feature/PRO-27-T5-validasi-backend
        ├── feature/PRO-28-T6-slicing-frontend
        └── ...
```

* **`main`**: Branch rilis resmi yang selalu stabil. Hanya menerima merge dari `test`.
* **`test`**: Branch bersama untuk integrasi seluruh stack dan pengujian akhir sprint.
* **`feature/<id-task>-<nama-singkat>`**: Branch lokal pengerjaan masing-masing task (dicabangkan dari `test`).

### 2. Aturan Kerja & Pull Request
1. **Dilarang keras push langsung ke branch `main` atau `test`**.
2. Setiap fitur dikerjakan di branch `feature/<id-task>-...`.
3. Setelah selesai dan unit test lulus di lokal, push ke remote dan buat **Pull Request (PR) ke branch `test`**.
4. CI Pipeline akan otomatis memvalidasi migrasi database dan menjalankan automated tests.
5. PR harus di-review sebelum di-merge ke branch `test`.

---

## ⚡ Quick Start (Setup Semi-Otomatis untuk Semua Stack)

Agar frontend, tester, maupun anggota tim lain tidak perlu melakukan setup manual yang rumit, telah disediakan script otomatis:

### 1. Clone Repository
```bash
git clone https://github.com/AsfiCorp/PPL_A_KEL2_M3.git
cd PPL_A_KEL2_M3
```

### 2. Jalankan Setup Semi-Otomatis (1 Perintah)
Cukup jalankan satu perintah berikut di terminal:
```bash
./setup.sh
```
Script ini secara otomatis akan:
1. Membuat virtual environment (`venv`).
2. Menginstal seluruh dependensi dari `requirements.txt`.
3. Menjalankan migrasi database SQLite (`python manage.py migrate`).
4. Menjalankan automated test suite untuk memastikan sistem siap dipakai.

### 3. Menjalankan Development Server
```bash
./venv/bin/python manage.py runserver
```
Server backend akan berjalan di: **`http://127.0.0.1:8000/`**

---

## 🎨 Panduan Khusus Frontend Developer

### Endpoint Pendaftaran Partner (Task T4 / M3-US1)
* **URL**: `http://127.0.0.1:8000/api/partners/register/`
* **Method**: `POST`
* **Headers**:
  * Jika hanya kirim data teks: `Content-Type: application/json`
  * Jika menyertakan unggahan file gambar: `Content-Type: multipart/form-data`

### Spesifikasi Field Formulir (Sesuai Desain Figma)
| Nama Field | Tipe Data | Wajib/Opsional | Deskripsi & Contoh |
| :--- | :--- | :--- | :--- |
| `nama_usaha` | String | **Wajib** | Nama toko/usaha (contoh: `"Toko Berkah"`) |
| `kategori_usaha` | String | **Wajib** | Pilihan dropdown: `"Produk"` atau `"Jasa"` |
| `deskripsi_usaha` | String | **Wajib** | Deskripsi singkat mengenai usaha |
| `alamat_usaha` | String | **Wajib** | Alamat fisik toko/usaha |
| `nomor_telepon_usaha` | String | **Wajib** | Nomor telepon/WhatsApp (contoh: `"081234567890"`) |
| `email_usaha` | String (Email) | **Wajib** | Email resmi usaha (harus unik) |
| `profil_usaha` | File (Image) | *Opsional* | File gambar format PNG, JPG, atau SVG |

### Format Respons API

#### 1. Respons Berhasil (`201 CREATED`)
```json
{
  "status": "success",
  "message": "Pendaftaran partner berhasil dikirim dan menunggu verifikasi.",
  "data": {
    "id": 1,
    "nama_usaha": "Toko Berkah Sejahtera",
    "kategori_usaha": "Produk",
    "deskripsi_usaha": "Menjual berbagai macam sembako kebutuhan harian.",
    "alamat_usaha": "Jl. Gatot Subroto No. 45, Bandung",
    "nomor_telepon_usaha": "081234567890",
    "email_usaha": "toko.berkah@example.com",
    "profil_usaha": null,
    "status": "pending",
    "created_at": "2026-10-28T15:34:00.123456Z"
  }
}
```

#### 2. Respons Gagal Validasi (`400 BAD REQUEST`)
```json
{
  "status": "error",
  "message": "Pendaftaran gagal. Silakan periksa kembali data yang diisi.",
  "errors": {
    "email_usaha": [
      "Partner with this Email usaha already exists."
    ]
  }
}
```

### Contoh Integrasi Frontend (JavaScript / Fetch)
```javascript
const formData = new FormData();
formData.append('nama_usaha', 'Toko Kue Enak');
formData.append('kategori_usaha', 'Produk');
formData.append('deskripsi_usaha', 'Aneka kue basah dan kering');
formData.append('alamat_usaha', 'Jl. Braga No. 10');
formData.append('nomor_telepon_usaha', '081234567899');
formData.append('email_usaha', 'tokokue@example.com');
// Jika ada file gambar:
// formData.append('profil_usaha', fileInput.files[0]);

fetch('http://127.0.0.1:8000/api/partners/register/', {
  method: 'POST',
  body: formData,
})
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      console.log('Status pendaftaran:', data.data.status); // 'pending'
      // Arahkan user ke halaman status pendaftaran berhasil
    } else {
      console.error('Error pendaftaran:', data.errors);
    }
  });
```

---

## 🧪 Panduan Khusus Tester & QA

Tester dapat menjalankan automated test suite menggunakan script berikut:

```bash
./run_test.sh
```
Atau secara manual:
```bash
./venv/bin/python manage.py test partners -v 2
```

### Cakupan Pengujian Unit Test Saat Ini (`partners/tests.py`)
1. **`test_post_partner_registration_success`**:
   * Memastikan endpoint `POST /api/partners/register/` mengembalikan HTTP `201 CREATED`.
   * Memastikan data tersimpan ke SQLite dengan status default `'pending'`.
2. **`test_post_partner_registration_authenticated_user`**:
   * Memastikan partner yang mendaftar saat login terasosiasi dengan akun `user` yang bersangkutan.
3. **`test_post_partner_registration_with_optional_image`**:
   * Memastikan unggahan berkas gambar profil (`multipart/form-data`) tersimpan dengan baik di sistem.

---

## ⚙️ CI/CD Pipeline (GitHub Actions)
Pipeline CI berada di file [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
Setiap ada `push` atau `PR` menuju `test` atau `main`, GitHub Actions akan:
1. Memeriksa migrasi Django (`python manage.py makemigrations --check --dry-run`).
2. Menjalankan seluruh automated test suite (`python manage.py test partners`).
3. Memastikan tidak ada kode yang merusak fungsionalitas yang sudah ada.
