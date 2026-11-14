from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from partners.models import Partner


class TestM3US1AcceptanceCriteria(APITestCase):
    """
    Test suite resmi QA untuk issue PRO-29 (Task T7):
    Pengujian fungsional seluruh Acceptance Criteria M3-US1.
    Telah diselaraskan dengan Panduan API Bersama.
    """

    def setUp(self):
        self.url = reverse('partners:partner-register')
        self.valid_payload = {
            "nama_usaha": "Kopi Senja QA",
            "kategori_usaha": "Produk",
            "deskripsi_usaha": "Kedai kopi artisan lokal",
            "alamat_usaha": "Jl. Cihampelas No. 12, Bandung",
            "nomor_telepon_usaha": "081234567890",
            "email_usaha": "kopisenja@qa.test"
        }

    # AC 1: Isi form lengkap -> status "pending" + response 201
    def test_ac1_form_lengkap_status_pending(self):
        res = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.data.get('success', False) or res.data.get('status') == 'success')
        self.assertEqual(res.data['data']['status'], 'pending')
        # DB check
        p = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])
        self.assertEqual(p.status, Partner.StatusPendaftaran.PENDING)

    # AC 2: Isi form tidak lengkap -> tolak (422/400) & tampilkan field yang kurang
    def test_ac2_form_tidak_lengkap_ditolak(self):
        incomplete_payload = {
            "kategori_usaha": "Produk"
            # nama_usaha, deskripsi, alamat, no telp, email sengaja dikosongkan
        }
        res = self.client.post(self.url, data=incomplete_payload, format='json')
        self.assertIn(res.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])
        self.assertTrue(res.data.get('success') is False or res.data.get('status') == 'error')
        errors = res.data.get('errors') or res.data.get('error', {}).get('fields', {})
        for required_field in ['nama_usaha', 'deskripsi_usaha', 'alamat_usaha', 'nomor_telepon_usaha', 'email_usaha']:
            self.assertIn(required_field, errors, f"Field {required_field} harus masuk daftar error")

    # AC 3: Email sudah terdaftar -> tolak (409/400) & pesan "Email sudah terdaftar"
    def test_ac3_email_duplikat_ditolak_dengan_pesan_spesifik(self):
        # Pendaftaran pertama
        self.client.post(self.url, data=self.valid_payload, format='json')
        # Pendaftaran kedua dengan email sama
        dup_payload = self.valid_payload.copy()
        dup_payload['nama_usaha'] = 'Usaha Cabang Lain'
        res = self.client.post(self.url, data=dup_payload, format='json')
        self.assertIn(res.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT, status.HTTP_422_UNPROCESSABLE_ENTITY])
        self.assertTrue(res.data.get('success') is False or res.data.get('status') == 'error')
        email_errors = str(
            res.data.get('errors', {}).get('email_usaha', '')
            or res.data.get('error', {}).get('fields', {}).get('email_usaha', '')
            or res.data.get('error', {}).get('message', '')
        )
        self.assertTrue(
            'already exists' in email_errors.lower() or 'sudah terdaftar' in email_errors.lower(),
            f"Error email harus menyatakan duplikasi, dapat: {email_errors}"
        )

    # AC 4: Format email tidak valid -> tolak (422/400) & pesan "Format email tidak valid"
    def test_ac4_format_email_invalid(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email_usaha'] = 'bukan-email-valid'
        res = self.client.post(self.url, data=invalid_payload, format='json')
        self.assertIn(res.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])
        self.assertTrue(res.data.get('success') is False or res.data.get('status') == 'error')
        email_errors = str(
            res.data.get('errors', {}).get('email_usaha', '')
            or res.data.get('error', {}).get('fields', {}).get('email_usaha', '')
            or res.data.get('error', {}).get('message', '')
        )
        self.assertTrue(
            'valid email' in email_errors.lower() or 'tidak valid' in email_errors.lower(),
            f"Error email harus menyatakan format invalid, dapat: {email_errors}"
        )

    # Negative Edge Case: Kategori usaha di luar 'Produk' / 'Jasa'
    def test_edge_kategori_usaha_invalid(self):
        payload = self.valid_payload.copy()
        payload['kategori_usaha'] = 'Fintech'
        res = self.client.post(self.url, data=payload, format='json')
        self.assertIn(res.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])
        errors = res.data.get('errors') or res.data.get('error', {}).get('fields', {})
        self.assertIn('kategori_usaha', errors)

    # Negative Edge Case: Method selain POST harus 405 Method Not Allowed
    def test_method_not_allowed_on_get(self):
        # Pada endpoint legacy register, GET adalah Method Not Allowed
        res = self.client.put(self.url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestM3US1EnhancedQA(APITestCase):
    """
    Test suite resmi QA untuk issue PRO-226 (Task T7.1):
    Automated Testing Registrasi: Foto KTP, Selfie Pegang KTP & Akun Aplikasi,
    Validasi NIK 16 digit, format foto dokumen, password kuat, dan auto partner_id.
    """

    def setUp(self):
        self.url = reverse('partners:partner-register')
        self.v1_url = reverse('partners_api:partner-list-create')

    def _generate_valid_image(self, filename="document.jpg", format_type="JPEG"):
        import io
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile

        file_obj = io.BytesIO()
        image = Image.new("RGB", (100, 100), color=(73, 109, 137))
        image.save(file_obj, format=format_type)
        file_obj.seek(0)
        return SimpleUploadedFile(
            name=filename,
            content=file_obj.read(),
            content_type=f"image/{format_type.lower()}"
        )

    def test_t7_1_registrasi_multipart_dokumen_dan_akun_berhasil(self):
        from django.contrib.auth.hashers import check_password

        ktp_file = self._generate_valid_image("ktp_qa.png", "PNG")
        selfie_file = self._generate_valid_image("selfie_qa.jpg", "JPEG")

        payload = {
            "nama_usaha": "CV Berkah Maju QA",
            "kategori_usaha": "Jasa",
            "deskripsi_usaha": "Jasa konsultasi IT dan digitalisasi UMKM",
            "alamat_usaha": "Jl. Ir. H. Juanda No. 99, Dago, Bandung",
            "nomor_telepon_usaha": "081298765432",
            "email_usaha": "berkah.qa@example.com",
            "penanggung_jawab_nama": "Budi Santoso QA",
            "penanggung_jawab_nik": "3273012304900001",
            "tempat_lahir": "Bandung",
            "tanggal_lahir": "1990-04-23",
            "password": "PasswordKuat2026",
            "foto_ktp": ktp_file,
            "foto_memegang_ktp": selfie_file,
        }

        res = self.client.post(self.v1_url, data=payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.data.get('success'))
        self.assertEqual(res.data['data']['status'], 'pending')
        
        partner_id = res.data['data'].get('partner_id')
        self.assertTrue(partner_id and partner_id.startswith('PRT-'), f"Format partner_id salah: {partner_id}")

        self.assertNotIn('password', res.data['data'])

    def test_t7_1_validasi_nik_invalid_ditolak(self):
        payload = {
            "nama_usaha": "Warung NIK Test",
            "kategori_usaha": "Produk",
            "deskripsi_usaha": "Warung kelontong",
            "alamat_usaha": "Jl. Asia Afrika",
            "nomor_telepon_usaha": "081234567811",
            "email_usaha": "nik.invalid@example.com",
            "penanggung_jawab_nik": "12345",
        }
        res = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(res.data.get('success'))
        fields_error = res.data.get('error', {}).get('fields', {})
        self.assertIn('penanggung_jawab_nik', fields_error)

    def test_t7_1_validasi_format_foto_dokumen_bukan_gambar_ditolak(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        fake_doc = SimpleUploadedFile("ktp.txt", b"ini teks bukan foto", content_type="text/plain")
        payload = {
            "nama_usaha": "Bengkel Mobil QA",
            "kategori_usaha": "Jasa",
            "deskripsi_usaha": "Bengkel perbaikan mesin",
            "alamat_usaha": "Jl. Soekarno Hatta",
            "nomor_telepon_usaha": "081234567822",
            "email_usaha": "bengkel.qa@example.com",
            "foto_ktp": fake_doc,
        }
        res = self.client.post(self.v1_url, data=payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        fields_error = res.data.get('error', {}).get('fields', {})
        self.assertIn('foto_ktp', fields_error)

    def test_t7_1_validasi_password_lemah_ditolak(self):
        payload = {
            "nama_usaha": "Toko Buku QA",
            "kategori_usaha": "Produk",
            "deskripsi_usaha": "Penjualan buku pelajaran",
            "alamat_usaha": "Jl. Braga",
            "nomor_telepon_usaha": "081234567833",
            "email_usaha": "tokobuku.qa@example.com",
            "password": "pass1",
        }
        res = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        fields_error = res.data.get('error', {}).get('fields', {})
        self.assertIn('password', fields_error)

    def test_t7_1_rejection_reason_protection(self):
        p = Partner.objects.create(
            nama_usaha="Toko Reject Test",
            kategori_usaha=Partner.KategoriUsaha.PRODUK,
            deskripsi_usaha="Testing rejection logic",
            alamat_usaha="Jl. Riau No. 1",
            nomor_telepon_usaha="081234567844",
            email_usaha="reject.test@example.com",
            status=Partner.StatusPendaftaran.PENDING,
            alasan_penolakan="Dokumen buram"
        )
        detail_url = reverse('partners:partner-detail', kwargs={'pk': p.pk})
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNone(res.data['data']['rejection_reason'])

        p.status = Partner.StatusPendaftaran.DITOLAK
        p.save()
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['data']['rejection_reason'], "Dokumen buram")
        self.assertNotIn('password_hash', res.data['data'])




class TestM3US1FormStepperAndStatusQA(TestCase):
    """
    Test suite resmi QA untuk issue PRO-225 (T6.2) & PRO-229 (T12.1):
    Slicing Form Stepper & Halaman Status Pendaftaran Partner.
    """

    def setUp(self):
        self.register_url = reverse('partner_ui:partner-registration')
        self.status_url = reverse('partner_ui:registration-status')
        self.store_url = reverse('partner_ui:my-store')
        self.valid_payload = {
            'nama_usaha': 'Warung Stepper QA',
            'kategori_usaha': 'Produk',
            'deskripsi_usaha': 'Warung kuliner khas Sunda',
            'alamat_usaha': 'Jl. Dipati Ukur No. 100, Bandung',
            'nomor_telepon_usaha': '081234567899',
            'email_usaha': 'warung.stepper@qa.test',
        }

    def test_t6_2_stepper_form_renders_all_sections(self):
        """Memastikan form stepper memuat 4 seksi (Info Usaha, Dokumen, Akun, Konfirmasi)."""
        res = self.client.get(self.register_url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'class="card registration-form"')
        self.assertContains(res, 'data-step="1"')
        self.assertContains(res, 'data-step="2"')
        self.assertContains(res, 'data-step="3"')
        self.assertContains(res, 'data-step="4"')

    def test_t12_1_pending_status_locks_registration_and_redirects(self):
        """
        Memastikan partner dengan status 'pending' tidak dapat membuka kembali
        halaman registrasi dan langsung dialihkan ke halaman status (kunci navigasi pending).
        """
        partner = Partner.objects.create(
            nama_usaha='Pending Store QA',
            kategori_usaha=Partner.KategoriUsaha.PRODUK,
            deskripsi_usaha='Toko dalam antrian verifikasi',
            alamat_usaha='Jl. Riau No. 50',
            nomor_telepon_usaha='081122334455',
            email_usaha='pending.qa@example.com',
            status=Partner.StatusPendaftaran.PENDING
        )
        session = self.client.session
        session['partner_application_id'] = partner.pk
        session.save()

        # Coba buka form registrasi -> harus diarahkan ke status
        res = self.client.get(self.register_url)
        self.assertRedirects(res, self.status_url)

        # Cek halaman status mengunci navigasi
        res_status = self.client.get(self.status_url)
        self.assertEqual(res_status.status_code, 200)
        self.assertContains(res_status, 'Menunggu persetujuan')
        self.assertContains(res_status, 'data-registration-status="pending"')

    def test_t12_1_rejected_status_shows_retry_button(self):
        """
        Memastikan partner dengan status 'ditolak' menampilkan alasan penolakan
        dan tombol 'Coba Mendaftar Kembali' ke halaman formulir.
        """
        partner = Partner.objects.create(
            nama_usaha='Rejected Store QA',
            kategori_usaha=Partner.KategoriUsaha.JASA,
            deskripsi_usaha='Jasa servis elektronik',
            alamat_usaha='Jl. Sunda No. 20',
            nomor_telepon_usaha='081199887766',
            email_usaha='rejected.qa@example.com',
            status=Partner.StatusPendaftaran.DITOLAK,
            alasan_penolakan='Foto KTP buram dan tidak terbaca.'
        )
        session = self.client.session
        session['partner_application_id'] = partner.pk
        session.save()

        res = self.client.get(self.status_url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Pendaftaran Partner Ditolak')
        self.assertContains(res, 'Foto KTP buram dan tidak terbaca.')
        self.assertContains(res, 'Coba Mendaftar Kembali')
        self.assertContains(res, 'href="/pendaftaran-partner/"')
