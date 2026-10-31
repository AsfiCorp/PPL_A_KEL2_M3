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
        self.assertEqual(response.data.get('status'), 'success')
        self.assertIn('data', response.data)
        self.assertEqual(response.data['data']['nama_usaha'], self.valid_payload['nama_usaha'])
        self.assertEqual(response.data['data']['email_usaha'], self.valid_payload['email_usaha'])
        self.assertEqual(response.data['data']['status'], 'pending')

        # Verifikasi data tersimpan di database
        partner = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])
        self.assertEqual(partner.status, Partner.StatusPendaftaran.PENDING)
        self.assertEqual(partner.nama_usaha, self.valid_payload['nama_usaha'])

    def test_post_partner_registration_authenticated_user(self):
        """
        Task T4: Menguji pendaftaran dengan user terotentikasi (opsional sesuai drawer profil).
        """
        user = User.objects.create_user(username='muhammad', email='muhammad@example.com', password='password123')
        self.client.force_authenticate(user=user)

        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        partner = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])
        self.assertEqual(partner.user, user)
        self.assertEqual(partner.status, 'pending')

    def test_post_partner_registration_with_optional_image(self):
        """
        Task T4: Menguji pendaftaran partner dengan upload profil usaha (opsional).
        """
        # Generate dummy image in memory
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
