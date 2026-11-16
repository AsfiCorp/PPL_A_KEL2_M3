-- ==============================================================================
-- Araya Business Hub - Modul 3: Manajemen Partner (Sprint 1 Supabase Schema)
-- Lingkup: M3-US1 (Pendaftaran Mandiri), M3-US3 (Cek Status), K-06 (Katalog Mitra)
-- ==============================================================================

-- 1. Buat Tabel partners
CREATE TABLE IF NOT EXISTS public.partners (
    id BIGSERIAL PRIMARY KEY,
    partner_id VARCHAR(30) UNIQUE NOT NULL,
    nama_usaha VARCHAR(255) NOT NULL,
    kategori_usaha VARCHAR(50) NOT NULL CHECK (kategori_usaha IN ('Produk', 'Jasa')),
    deskripsi_usaha TEXT NOT NULL,
    alamat_usaha TEXT NOT NULL,
    nomor_telepon_usaha VARCHAR(30) NOT NULL,
    email_usaha VARCHAR(255) UNIQUE NOT NULL,
    profil_usaha TEXT,
    nama_lengkap VARCHAR(255),
    nik VARCHAR(16),
    tempat_lahir VARCHAR(100),
    tanggal_lahir DATE,
    ktp TEXT,
    foto_pemegang_ktp TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'terverifikasi', 'ditolak', 'ditangguhkan')),
    alasan_penolakan TEXT,
    alasan_penangguhan TEXT,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Indeks untuk pencarian cepat
CREATE INDEX IF NOT EXISTS idx_partners_status ON public.partners (status);
CREATE INDEX IF NOT EXISTS idx_partners_partner_id ON public.partners (partner_id);
CREATE INDEX IF NOT EXISTS idx_partners_email_usaha ON public.partners (email_usaha);

-- 2. Aktifkan Row Level Security (RLS)
ALTER TABLE public.partners ENABLE ROW LEVEL SECURITY;

-- Policy 1: Publik (Anon) dapat membaca katalog partner terverifikasi (Kontrak K-06)
DROP POLICY IF EXISTS "Public can view verified partners" ON public.partners;
CREATE POLICY "Public can view verified partners"
    ON public.partners
    FOR SELECT
    TO anon, authenticated
    USING (status = 'terverifikasi');

-- Policy 2: Publik (Anon) dapat membaca status pendaftarannya sendiri berdasarkan partner_id (M3-US3)
DROP POLICY IF EXISTS "Public can view application status by partner_id" ON public.partners;
CREATE POLICY "Public can view application status by partner_id"
    ON public.partners
    FOR SELECT
    TO anon, authenticated
    USING (partner_id IS NOT NULL);

-- Policy 3: Publik (Anon) dapat mendaftarkan partner baru (M3-US1) dengan status default 'pending'
DROP POLICY IF EXISTS "Public can register partner application" ON public.partners;
CREATE POLICY "Public can register partner application"
    ON public.partners
    FOR INSERT
    TO anon, authenticated
    WITH CHECK (status = 'pending');

-- 3. Data Seed / Dummy untuk Pengujian Frontend Sprint 1
INSERT INTO public.partners (
    partner_id,
    nama_usaha,
    kategori_usaha,
    deskripsi_usaha,
    alamat_usaha,
    nomor_telepon_usaha,
    email_usaha,
    status,
    alasan_penolakan
) VALUES 
-- Contoh 1: Mitra Terverifikasi (Katalog K-06)
(
    'PRT-20261108-A101',
    'Toko Roti Barokah',
    'Produk',
    'Menjual aneka roti tawar, bolu, dan pastry segar setiap hari.',
    'Jl. Lengkong Besar No. 45, Bandung',
    '081234567801',
    'roti.barokah@example.com',
    'terverifikasi',
    NULL
),
-- Contoh 2: Mitra Terverifikasi (Katalog K-06)
(
    'PRT-20261108-B202',
    'Klinik Servis Elektronik Cepat',
    'Jasa',
    'Melayani perbaikan laptop, printer, dan smartphone bergaransi.',
    'Jl. Dipati Ukur No. 88, Bandung',
    '081234567802',
    'servis.cepat@example.com',
    'terverifikasi',
    NULL
),
-- Contoh 3: Mitra Menunggu Verifikasi (Pending M3-US3)
(
    'PRT-20261108-C303',
    'Warung Kopi Nusantara',
    'Produk',
    'Kedai kopi artisan dengan biji kopi pilihan nusantara.',
    'Jl. Dago No. 120, Bandung',
    '081234567803',
    'kopi.nusantara@example.com',
    'pending',
    NULL
),
-- Contoh 4: Mitra Ditolak dengan Alasan (M3-US3 AC 2)
(
    'PRT-20261108-D404',
    'Bimbingan Belajar Juara',
    'Jasa',
    'Les privat dan bimbingan belajar untuk tingkat SD, SMP, SMA.',
    'Jl. Buah Batu No. 15, Bandung',
    '081234567804',
    'bimbel.juara@example.com',
    'ditolak',
    'Foto KTP buram dan NIK tidak sesuai dengan data identitas penanggung jawab.'
)
ON CONFLICT (partner_id) DO NOTHING;
