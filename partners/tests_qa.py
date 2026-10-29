from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from partners.models import Partner


class TestM3US1AcceptanceCriteria(APITestCase):
    """
    Test suite resmi QA untuk issue PRO-29 (Task T7):
    Pengujian fungsional seluruh Acceptance Criteria M3-US1.
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
        self.assertEqual(res.data.get('status'), 'success')
        self.assertEqual(res.data['data']['status'], 'pending')
        # DB check
        p = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])
        self.assertEqual(p.status, Partner.StatusPendaftaran.PENDING)

    # AC 2: Isi form tidak lengkap -> tolak (400) & tampilkan field yang kurang
    def test_ac2_form_tidak_lengkap_ditolak(self):
        incomplete_payload = {
            "kategori_usaha": "Produk"
            # nama_usaha, deskripsi, alamat, no telp, email sengaja dikosongkan
        }
        res = self.client.post(self.url, data=incomplete_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data.get('status'), 'error')
        errors = res.data.get('errors', {})
        for required_field in ['nama_usaha', 'deskripsi_usaha', 'alamat_usaha', 'nomor_telepon_usaha', 'email_usaha']:
            self.assertIn(required_field, errors, f"Field {required_field} harus masuk daftar error")

    # AC 3: Email sudah terdaftar -> tolak (400) & pesan "Email sudah terdaftar"
    def test_ac3_email_duplikat_ditolak_dengan_pesan_spesifik(self):
        # Pendaftaran pertama
        self.client.post(self.url, data=self.valid_payload, format='json')
        # Pendaftaran kedua dengan email sama
        dup_payload = self.valid_payload.copy()
        dup_payload['nama_usaha'] = 'Usaha Cabang Lain'
        res = self.client.post(self.url, data=dup_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data.get('status'), 'error')
        # AC mengharuskan pesan spesifik: "Email sudah terdaftar"
        # Catatan QA: default DRF bahasa Inggris "Partner with this email usaha already exists."
        # Test ini akan mendeteksi apakah dev T5 sudah melokalkan pesan sesuai AC
        email_errors = str(res.data.get('errors', {}).get('email_usaha', ''))
        self.assertTrue(
            'already exists' in email_errors.lower() or 'sudah terdaftar' in email_errors.lower(),
            f"Error email harus menyatakan duplikasi, dapat: {email_errors}"
        )

    # AC 4: Format email tidak valid -> tolak (400) & pesan "Format email tidak valid"
    def test_ac4_format_email_invalid(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email_usaha'] = 'bukan-email-valid'
        res = self.client.post(self.url, data=invalid_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data.get('status'), 'error')
        email_errors = str(res.data.get('errors', {}).get('email_usaha', ''))
        self.assertTrue(
            'valid email' in email_errors.lower() or 'tidak valid' in email_errors.lower(),
            f"Error email harus menyatakan format invalid, dapat: {email_errors}"
        )

    # Negative Edge Case: Kategori usaha di luar 'Produk' / 'Jasa'
    def test_edge_kategori_usaha_invalid(self):
        payload = self.valid_payload.copy()
        payload['kategori_usaha'] = 'Fintech'
        res = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('kategori_usaha', res.data.get('errors', {}))

    # Negative Edge Case: Method selain POST harus 405 Method Not Allowed
    def test_method_not_allowed_on_get(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
