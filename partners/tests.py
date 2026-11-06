import io
from PIL import Image
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Partner

User = get_user_model()


class PartnerRegistrationAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('partners:partner-register')
        self.v1_url = reverse('partners_api:partner-list-create')
        self.valid_payload = {
            "nama_usaha": "Toko Berkah Sejahtera",
            "kategori_usaha": "Produk",
            "deskripsi_usaha": "Menjual berbagai macam kebutuhan pokok dan produk retail lokal.",
            "alamat_usaha": "Jl. Gatot Subroto No. 45, Bandung",
            "nomor_telepon_usaha": "081234567890",
            "email_usaha": "toko.berkah@example.com"
        }

    def test_post_partner_registration_success(self):
        """
        Task T4: Menguji pembuatan Partner baru via POST.
        Memastikan response status 201 Created dan status awal pendaftaran adalah 'pending'.
        """
        response = self.client.post(self.url, data=self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('success', False) or response.data.get('status') == 'success')
        self.assertIn('data', response.data)
        self.assertEqual(response.data['data']['nama_usaha'], self.valid_payload['nama_usaha'])
        self.assertEqual(response.data['data']['email_usaha'], self.valid_payload['email_usaha'])
        self.assertEqual(response.data['data']['status'], 'pending')

        partner = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])
        self.assertEqual(partner.status, Partner.StatusPendaftaran.PENDING)
        self.assertEqual(partner.nama_usaha, self.valid_payload['nama_usaha'])

    def test_post_partner_registration_v1_contract_compliance(self):
        """
        Menguji endpoint standar v1: POST /api/m3/v1/partners/
        Sesuai Panduan API Bersama: amplop success: true dan HTTP 201 Created.
        """
        response = self.client.post(self.v1_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('success'))
        self.assertIn('data', response.data)
        self.assertEqual(response.data['data']['status'], 'pending')

    def test_post_partner_registration_v1_error_envelope_422(self):
        """
        Menguji galat validasi field kosong pada v1:
        Sesuai Panduan API Bersama: status 422, amplop success: false, error.code, error.fields.
        """
        invalid_payload = {
            "kategori_usaha": "Produk"
        }
        response = self.client.post(self.v1_url, data=invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(response.data['success'])
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
        self.assertIn('nama_usaha', response.data['error']['fields'])

    def test_post_partner_registration_v1_duplicate_email_409(self):
        """
        Menguji galat duplikasi email:
        Sesuai Panduan API Bersama: status 409 Conflict, code EMAIL_DUPLICATE.
        """
        self.client.post(self.v1_url, data=self.valid_payload, format='json')
        response = self.client.post(self.v1_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error']['code'], 'EMAIL_DUPLICATE')
        self.assertEqual(response.data['error']['message'], 'Email sudah terdaftar.')

    def test_get_partners_catalog_k06_contract(self):
        """
        Menguji Kontrak K-06: GET /api/m3/v1/partners?status=terverifikasi
        """
        Partner.objects.create(
            nama_usaha="Toko Aktif 1",
            kategori_usaha="Produk",
            deskripsi_usaha="Deskripsi toko.",
            alamat_usaha="Alamat toko.",
            nomor_telepon_usaha="081234567891",
            email_usaha="aktif1@example.com",
            status=Partner.StatusPendaftaran.TERVERIFIKASI
        )
        Partner.objects.create(
            nama_usaha="Toko Pending 2",
            kategori_usaha="Produk",
            deskripsi_usaha="Deskripsi toko.",
            alamat_usaha="Alamat toko.",
            nomor_telepon_usaha="081234567892",
            email_usaha="pending2@example.com",
            status=Partner.StatusPendaftaran.PENDING
        )

        response = self.client.get(f"{self.v1_url}?status=terverifikasi")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['nama_usaha'], "Toko Aktif 1")
        self.assertIn('meta', response.data)
        self.assertEqual(response.data['meta']['total'], 1)

    def test_t10_get_partner_status_by_id_pending(self):
        """
        Task T10: GET status pendaftaran partner berdasarkan ID (status pending).
        """
        partner = Partner.objects.create(
            nama_usaha="Toko Uji Pending",
            kategori_usaha="Produk",
            deskripsi_usaha="Deskripsi.",
            alamat_usaha="Alamat.",
            nomor_telepon_usaha="081234567894",
            email_usaha="pending@example.com",
            status=Partner.StatusPendaftaran.PENDING
        )
        url = reverse('partners_api:partner-detail', kwargs={'pk': partner.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['success'])
        self.assertEqual(res.data['data']['status'], 'pending')
        self.assertIsNone(res.data['data']['alasan_penolakan'])

    def test_t10_get_partner_status_by_id_rejected_with_reason(self):
        """
        Task T10 / M3-US3 AC 2: GET status pendaftaran ditolak menampilkan alasan penolakan.
        """
        partner = Partner.objects.create(
            nama_usaha="Toko Uji Ditolak",
            kategori_usaha="Jasa",
            deskripsi_usaha="Deskripsi.",
            alamat_usaha="Alamat.",
            nomor_telepon_usaha="081234567895",
            email_usaha="ditolak@example.com",
            status=Partner.StatusPendaftaran.DITOLAK,
            alasan_penolakan="Berkas NIB tidak valid atau belum terlampir."
        )
        url = reverse('partners_api:partner-detail', kwargs={'pk': partner.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['success'])
        self.assertEqual(res.data['data']['status'], 'ditolak')
        self.assertEqual(res.data['data']['alasan_penolakan'], "Berkas NIB tidak valid atau belum terlampir.")

    def test_t10_get_partner_status_by_id_not_found(self):
        """
        Task T10: GET partner dengan ID yang tidak ada mengembalikan 404 dan amplop error.
        """
        url = reverse('partners_api:partner-detail', kwargs={'pk': 99999})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(res.data['success'])
        self.assertEqual(res.data['error']['code'], 'PARTNER_NOT_FOUND')

    def test_openapi_and_docs_endpoints(self):
        """
        Menguji ketersediaan halaman dokumentasi Swagger dan schema OpenAPI.
        """
        docs_res = self.client.get(reverse('api-docs'))
        self.assertEqual(docs_res.status_code, status.HTTP_200_OK)
        self.assertIn('swagger-ui', docs_res.content.decode('utf-8'))

        schema_res = self.client.get(reverse('openapi-yaml'))
        self.assertEqual(schema_res.status_code, status.HTTP_200_OK)
        self.assertIn('openapi: 3.0.3', schema_res.content.decode('utf-8'))

    def test_post_partner_registration_authenticated_user(self):
        user = User.objects.create_user(username='muhammad', email='muhammad@example.com', password='password123')
        self.client.force_authenticate(user=user)

        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        partner = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])
        self.assertEqual(partner.user, user)
        self.assertEqual(partner.status, 'pending')

    def test_post_partner_registration_with_optional_image(self):
        image_file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='blue')
        image.save(image_file, 'png')
        image_file.seek(0)
        uploaded_image = SimpleUploadedFile('profil.png', image_file.read(), content_type='image/png')

        payload = self.valid_payload.copy()
        payload['email_usaha'] = 'toko.gambar@example.com'
        payload['profil_usaha'] = uploaded_image

        response = self.client.post(self.url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        partner = Partner.objects.get(email_usaha='toko.gambar@example.com')
        self.assertTrue(bool(partner.profil_usaha))
        self.assertEqual(partner.status, 'pending')


class PartnerRegistrationUITestCase(TestCase):
    def setUp(self):
        self.form_url = reverse('partner_ui:partner-registration')
        self.valid_payload = {
            'nama_usaha': 'Toko UI Test',
            'kategori_usaha': 'Produk',
            'deskripsi_usaha': 'Produk lokal berkualitas.',
            'alamat_usaha': 'Jl. Merdeka No. 1',
            'nomor_telepon_usaha': '081234567890',
            'email_usaha': 'ui@example.com',
        }

    def test_ui_pages_render(self):
        self.assertEqual(self.client.get(reverse('partner_ui:home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('partner_ui:my-store')).status_code, 200)
        response = self.client.get(self.form_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Informasi usaha')
        self.assertContains(response, 'multipart/form-data')

    def test_registration_shows_pending_status(self):
        response = self.client.post(self.form_url, self.valid_payload)
        partner = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('partner_ui:registration-status'))
        self.assertEqual(partner.status, Partner.StatusPendaftaran.PENDING)

        status_response = self.client.get(response.url)
        self.assertEqual(status_response.status_code, 200)
        self.assertContains(status_response, 'Pendaftaran berhasil dikirim')
        self.assertContains(status_response, 'Toko UI Test')
        self.assertContains(status_response, 'Menunggu persetujuan')

    def test_invalid_registration_renders_field_errors(self):
        response = self.client.post(self.form_url, {
            **self.valid_payload,
            'nama_usaha': '',
            'email_usaha': 'bukan-email',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('nama_usaha', response.context['form'].errors)
        self.assertIn('email_usaha', response.context['form'].errors)
        self.assertEqual(Partner.objects.count(), 0)

    def test_duplicate_email_is_rejected(self):
        Partner.objects.create(
            nama_usaha='Usaha lain',
            kategori_usaha='Jasa',
            deskripsi_usaha='Layanan.',
            alamat_usaha='Jl. Merdeka No. 2',
            nomor_telepon_usaha='081234567891',
            email_usaha=self.valid_payload['email_usaha'],
        )

        response = self.client.post(self.form_url, self.valid_payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn('email_usaha', response.context['form'].errors)
        self.assertEqual(Partner.objects.count(), 1)
