# Panduan Integrasi Supabase - Modul 3 (Araya M3 - Sprint 1)

Proyek Supabase resmi untuk **Modul 3 (Araya M3)** telah berhasil dibuat dan terkonfigurasi di *cloud* untuk kebutuhan **Sprint 1**. Basis data ini dapat langsung diakses oleh tim **Frontend** via REST API / SDK Supabase maupun oleh **Backend Django**.

---

## 1. Kredensial Proyek Supabase (Live)

| Parameter | Nilai Resmi |
| :--- | :--- |
| **Nama Proyek** | `Araya M3` |
| **Project Ref** | `ahemuctnwslwikbqyyrv` |
| **Dashboard URL** | [supabase.com/dashboard/project/ahemuctnwslwikbqyyrv](https://supabase.com/dashboard/project/ahemuctnwslwikbqyyrv) |
| **Region** | `ap-southeast-1` (Singapore) |
| **API URL (Project URL)** | `https://ahemuctnwslwikbqyyrv.supabase.co` |
| **Anon Public Key** | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFoZW11Y3Rud3Nsd2lrYnF5eXJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ4MTAzNjUsImV4cCI6MjExMDM4NjM2NX0.e0sLYg9uI7AMnRYgfxq_7T284lo3KgHDuPuiVgeGzGA` |
| **Database Host** | `aws-0-ap-southeast-1.pooler.supabase.com` (Port `6543`) |
| **Database User** | `postgres.ahemuctnwslwikbqyyrv` |
| **Database Name** | `postgres` |

---

## 2. Cara Pakai Langsung untuk Tim Frontend

Frontend dapat langsung membaca dan menulis data ke tabel `partners` tanpa perlu menjalankan backend Django lokal.

### Pemasangan SDK Supabase
```bash
npm install @supabase/supabase-js
```

### Inisialisasi Klien (Frontend)
```javascript
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://ahemuctnwslwikbqyyrv.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFoZW11Y3Rud3Nsd2lrYnF5eXJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ4MTAzNjUsImV4cCI6MjExMDM4NjM2NX0.e0sLYg9uI7AMnRYgfxq_7T284lo3KgHDuPuiVgeGzGA';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
```

### A. Mengambil Katalog Partner Terverifikasi (Kontrak K-06)
```javascript
// Mengambil toko aktif untuk etalase publik Modul 5
const { data: partners, error } = await supabase
  .from('partners')
  .select('partner_id, nama_usaha, kategori_usaha, deskripsi_usaha, alamat_usaha, nomor_telepon_usaha, email_usaha')
  .eq('status', 'terverifikasi')
  .order('created_at', { ascending: false });

console.log('Katalog Toko:', partners);
```

### B. Pelacakan Status Pendaftaran Mandiri (M3-US3)
```javascript
// Pelacakan status pendaftaran berdasarkan partner_id
const { data: application, error } = await supabase
  .from('partners')
  .select('partner_id, nama_usaha, status, alasan_penolakan, created_at')
  .eq('partner_id', 'PRT-20261108-C303')
  .single();

console.log('Status Pendaftaran:', application.status);
```

### C. Pendaftaran Partner Baru (M3-US1)
```javascript
const newApplication = {
  partner_id: `PRT-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-${Math.random().toString(16).substring(2, 6).toUpperCase()}`,
  nama_usaha: 'Toko Baru Mandiri',
  kategori_usaha: 'Produk', // 'Produk' atau 'Jasa'
  deskripsi_usaha: 'Menjual aneka sembako murah',
  alamat_usaha: 'Jl. Merdeka No. 12, Bandung',
  nomor_telepon_usaha: '081234567800',
  email_usaha: 'tokobaru@example.com',
  status: 'pending' // Wajib 'pending' sesuai aturan RLS
};

const { data, error } = await supabase
  .from('partners')
  .insert([newApplication]);
```

---

## 3. Cara Menghubungkan Backend Django

Backend Django Modul 3 telah dikonfigurasi menggunakan `dj-database-url`.

Cukup set variabel lingkungan sebelum menjalankan server (atau pasang di dashboard PythonAnywhere):
```bash
export DATABASE_URL="postgresql://postgres.ahemuctnwslwikbqyyrv:arayamodul3@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
```

Jika variabel `DATABASE_URL` tidak diset, backend secara otomatis beralih ke SQLite lokal (`db.sqlite3`) untuk memastikan unit test tetap berjalan cepat dan offline.
