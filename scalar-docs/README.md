# Panduan Deploy Dokumentasi API Scalar ke Vercel

Folder ini berisi dokumentasi interaktif resmi RESTful API Modul 3 (Manajemen Partner) Araya Business Hub menggunakan **Scalar API Reference**.

---

## Isi Berkas
- `index.html`: Berkas web mandiri (*standalone*) Scalar API Reference yang siap pakai.
- `openapi.yaml`: Kontrak spesifikasi OpenAPI 3.0.3 lengkap untuk Modul 3.
- `vercel.json`: Konfigurasi routing static dan header CORS untuk Vercel.
- `package.json`: Konfigurasi proyek statis.

---

## Cara 1: Deploy Sangat Cepat via Vercel CLI (Direkomendasikan)
1. Buka terminal dan masuk ke folder `scalar-docs`:
   ```bash
   cd scalar-docs
   ```
2. Jalankan perintah deploy Vercel:
   ```bash
   npx vercel
   ```
   *(atau `npx vercel --prod` untuk langsung rilis ke domain produksi).*
3. Ikuti prompt singkat di terminal (cukup tekan Enter untuk pilihan default).
4. Dokumentasi API Scalar Anda langsung online dengan URL: `https://<nama-proyek>.vercel.app`!

---

## Cara 2: Deploy via Vercel Dashboard (GitHub / Drag & Drop)
1. Buka [vercel.com](https://vercel.com) dan login ke akun Anda.
2. Klik tombol **Add New...** -> **Project**.
3. Hubungkan repository GitHub Anda.
4. Pada bagian **Root Directory**, klik **Edit** dan pilih folder `scalar-docs`.
5. Klik **Deploy**. Selesai!

---

## Cara 3: Uji Coba Pratinjau Lokal di Komputer
Anda dapat menguji halaman dokumentasi ini di komputer lokal sebelum dideploy:
1. Jalankan web server lokal bawaan Python:
   ```bash
   cd scalar-docs
   python3 -m http.server 3000
   ```
2. Buka peramban di `http://localhost:3000`.
   *(Atau Anda juga dapat langsung klik dua kali berkas `index.html` untuk membukanya di browser!)*
