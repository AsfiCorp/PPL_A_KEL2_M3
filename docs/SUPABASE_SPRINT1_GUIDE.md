# Panduan Integrasi Supabase - Modul 3 (Sprint 1)

Dokumentasi ini menjelaskan cara menggunakan **Supabase PostgreSQL** sebagai basis data terpusat Modul 3 agar tim **Frontend** dapat langsung mengonsumsi data secara mandiri tanpa tergantung pada server lokal backend, serta cara **Backend Django** terhubung ke basis data yang sama.

---

## 1. Lingkup Data Sprint 1
Sesuai batasan Sprint 1, skema dan data Supabase hanya mencakup:
- **M3-US1**: Pendaftaran Mandiri Calon Partner Baru.
- **M3-US3**: Detail dan Pelacakan Status Pendaftaran (Pending / Terverifikasi / Ditolak).
- **K-06**: Penyediaan Data Katalog Partner Terverifikasi untuk Modul 5 dan Modul 4.

---

## 2. Setup Instan di Supabase (Untuk Frontend & Database)

1. Buka dashboard proyek Supabase Anda di [supabase.com](https://supabase.com).
2. Masuk ke menu **SQL Editor** pada panel navigasi kiri.
3. Buka berkas [`docs/supabase_sprint1_setup.sql`](./supabase_sprint1_setup.sql), salin seluruh isinya, lalu tempelkan ke SQL Editor.
4. Klik **Run**.
5. Tabel `partners` otomatis terbentuk lengkap dengan:
   - Struktur kolom Sprint 1.
   - Aturan keamanan **Row Level Security (RLS)** untuk publik (`anon`).
   - 4 baris data uji (*seed data*): 2 toko aktif (*terverifikasi*), 1 toko *pending*, dan 1 toko *ditolak*.

---

## 3. Contoh Konsumsi Data oleh Frontend (`@supabase/supabase-js`)

Frontend dapat langsung memasang SDK Supabase:
```bash
npm install @supabase/supabase-js
```

Inisialisasi klien:
```javascript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL; // atau VITE_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

### A. Mengambil Katalog Partner Terverifikasi (Kontrak K-06)
```javascript
// Dipanggil oleh Frontend Modul 5 / Halaman Katalog
const { data: catalog, error } = await supabase
  .from('partners')
  .select('*')
  .eq('status', 'terverifikasi')
  .order('created_at', { ascending: false });

console.log('Katalog Toko Terverifikasi:', catalog);
```

### B. Pelacakan Status Pendaftaran (M3-US3)
```javascript
// Pengguna memasukkan kode partner_id (contoh: PRT-20261108-C303)
const { data: partner, error } = await supabase
  .from('partners')
  .select('partner_id, nama_usaha, status, alasan_penolakan, created_at')
  .eq('partner_id', 'PRT-20261108-C303')
  .single();

if (partner) {
  console.log(`Status Pengajuan: ${partner.status}`);
  if (partner.status === 'ditolak') {
    console.log(`Alasan Penolakan: ${partner.alasan_penolakan}`);
  }
}
```

### C. Pendaftaran Partner Baru (M3-US1)
```javascript
const newPartner = {
  partner_id: `PRT-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-${Math.random().toString(16).substring(2, 6).toUpperCase()}`,
  nama_usaha: 'Toko Baru Saya',
  kategori_usaha: 'Produk',
  deskripsi_usaha: 'Menjual barang kebutuhan pokok berkualitas',
  alamat_usaha: 'Jl. Merdeka No. 1, Bandung',
  nomor_telepon_usaha: '081234567899',
  email_usaha: 'tokobaru@example.com',
  status: 'pending' // Wajib pending sesuai kebijakan RLS
};

const { data, error } = await supabase
  .from('partners')
  .insert([newPartner]);
```

---

## 4. Menghubungkan Backend Django ke Supabase

Backend Django Modul 3 telah dilengkapi dengan adapter `dj-database-url` dan `psycopg2-binary`.

1. Di Supabase, masuk ke **Project Settings** > **Database**.
2. Cari bagian **Connection string** > pilih tab **URI**.
3. Salin URI tersebut, lalu set variabel lingkungan `DATABASE_URL` di lokal atau hosting backend (PythonAnywhere):
   ```bash
   export DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
   ```
4. Jalankan migrasi:
   ```bash
   ./venv/bin/python manage.py migrate
   ```
5. Jika variabel `DATABASE_URL` tidak diset, Django secara otomatis tetap memakai SQLite lokal (`db.sqlite3`) sehingga pengujian unit test dan pengembangan offline tetap 100% aman.
