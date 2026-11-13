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
        self.assertEqual(self.client.session['partner_application_id'], partner.pk)

    def test_api_validation_errors_are_returned_for_ui(self):
        response = self.client.post(self.url, {
            **self.valid_payload,
            'nama_usaha': '',
            'email_usaha': 'bukan-email',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nama_usaha', response.data['errors'])
        self.assertIn('email_usaha', response.data['errors'])

    def test_api_submission_can_render_registration_status_page(self):
        response = self.client.post(self.url, data=self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        status_response = self.client.get(reverse('partner_ui:registration-status'))

        self.assertEqual(status_response.status_code, 200)
        self.assertContains(status_response, self.valid_payload['nama_usaha'])
        self.assertContains(status_response, 'Menunggu persetujuan')

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
        self.assertEqual(res.data['data']['rejection_reason'], "Berkas NIB tidak valid atau belum terlampir.")

    def test_t11_rejection_reason_null_when_status_not_ditolak(self):
        """
        Task T11: Backend logic memastikan rejection_reason bernilai null bila status bukan 'ditolak'.
        """
        partner = Partner.objects.create(
            nama_usaha="Toko Uji Terverifikasi",
            kategori_usaha="Produk",
            deskripsi_usaha="Deskripsi.",
            alamat_usaha="Alamat.",
            nomor_telepon_usaha="081234567896",
            email_usaha="verif@example.com",
            status=Partner.StatusPendaftaran.TERVERIFIKASI
        )
        url = reverse('partners_api:partner-detail', kwargs={'pk': partner.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNone(res.data['data']['rejection_reason'])
        self.assertIsNone(res.data['data']['alasan_penolakan'])

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

    def test_completed_registration_creates_account_and_saves_responsible_documents(self):
        payload = {
            **self.valid_payload,
            'email_usaha': 'toko.lengkap@example.com',
            'complete_registration': 'true',
            'nama_lengkap': 'Siti Aminah',
            'nik': '3201010101010001',
            'tempat_lahir': 'Bandung',
            'tanggal_lahir': '1995-04-12',
            'ktp': SimpleUploadedFile('ktp.pdf', b'%PDF-1.4 ktp', content_type='application/pdf'),
            'foto_pemegang_ktp': SimpleUploadedFile(
                'pemegang-ktp.jpg',
                b'foto pemegang ktp',
                content_type='image/jpeg',
            ),
            'account_email': 'siti.account@example.com',
            'password': 'S3cure!LongPassword-2026',
            'confirm_password': 'S3cure!LongPassword-2026',
        }

        response = self.client.post(self.url, data=payload, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        partner = Partner.objects.get(email_usaha=payload['email_usaha'])
        self.addCleanup(partner.ktp.delete, save=False)
        self.addCleanup(partner.foto_pemegang_ktp.delete, save=False)
        self.assertEqual(partner.nama_lengkap, payload['nama_lengkap'])
        self.assertEqual(partner.nik, payload['nik'])
        self.assertEqual(partner.tempat_lahir, payload['tempat_lahir'])
        self.assertEqual(str(partner.tanggal_lahir), payload['tanggal_lahir'])
        self.assertTrue(partner.ktp)
        self.assertTrue(partner.foto_pemegang_ktp)
        self.assertEqual(partner.user.email, payload['account_email'])
        self.assertTrue(partner.user.check_password(payload['password']))

    def test_completed_registration_rejects_mismatched_passwords(self):
        response = self.client.post(self.url, {
            **self.valid_payload,
            'complete_registration': 'true',
            'nama_lengkap': 'Siti Aminah',
            'nik': '3201010101010001',
            'tempat_lahir': 'Bandung',
            'tanggal_lahir': '1995-04-12',
            'ktp': SimpleUploadedFile('ktp.pdf', b'%PDF-1.4 ktp', content_type='application/pdf'),
            'foto_pemegang_ktp': SimpleUploadedFile(
                'pemegang-ktp.pdf',
                b'%PDF-1.4 photo',
                content_type='application/pdf',
            ),
            'account_email': 'siti.account@example.com',
            'password': 'S3cure!LongPassword-2026',
            'confirm_password': 'Different!Password-2026',
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data['errors'])
        self.assertFalse(User.objects.filter(email='siti.account@example.com').exists())


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
        store_response = self.client.get(reverse('partner_ui:my-store'))
        self.assertEqual(store_response.status_code, 200)
        self.assertContains(store_response, 'Pendaftaran partner')
        response = self.client.get(self.form_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Informasi Usaha')
        self.assertContains(response, 'multipart/form-data')
        self.assertContains(response, 'data-api-url="/api/partners/register/"')
        self.assertContains(response, 'data-field-errors="email_usaha"')
        self.assertContains(response, 'Dokumen Pendukung')
        self.assertContains(response, 'Konfirmasi Pendaftaran')
        self.assertContains(response, 'name="account_email"')
        self.assertContains(response, 'name="foto_pemegang_ktp"')

    def test_profile_drawer_is_available_and_closed_by_default(self):
        response = self.client.get(reverse('partner_ui:home'))

        self.assertContains(response, 'aria-controls="profile-drawer"')
        self.assertContains(response, 'aria-expanded="false"')
        self.assertContains(response, 'id="profile-drawer"')
        self.assertContains(response, 'Menu Pengguna')
        self.assertContains(response, 'Pesanan Saya')
        self.assertContains(response, 'Notifikasi')
        self.assertContains(response, 'Pengaturan')
        self.assertContains(response, 'Toko Saya')
        self.assertContains(response, 'href="/pendaftaran-partner/"')
        self.assertContains(response, 'Pendaftaran Partner')
        self.assertContains(response, 'class="profile-drawer"')
        self.assertContains(response, 'aria-hidden="true"')

    def test_authenticated_user_can_log_out_from_profile_drawer(self):
        user = User.objects.create_user(username='drawer-user', password='password123')
        self.client.force_login(user)

        response = self.client.post(reverse('partner_ui:logout'))

        self.assertRedirects(response, reverse('partner_ui:home'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_registration_shows_pending_status(self):
        response = self.client.post(self.form_url, self.valid_payload)
        partner = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('partner_ui:registration-status'))
        self.assertEqual(partner.status, Partner.StatusPendaftaran.PENDING)

        status_response = self.client.get(response.url)
        self.assertEqual(status_response.status_code, 200)
        self.assertContains(status_response, 'Pendaftaran Berhasil Dikirim')
        self.assertContains(status_response, 'Toko UI Test')
        self.assertContains(status_response, 'Menunggu persetujuan')
        self.assertContains(status_response, 'Tim Araya Business Hub akan meninjau')

        partner.status = Partner.StatusPendaftaran.TERVERIFIKASI
        partner.save(update_fields=['status', 'updated_at'])
        verified_response = self.client.get(response.url)
        self.assertContains(verified_response, 'Pendaftaran Partner Berhasil Diverifikasi')
        self.assertContains(verified_response, 'Terverifikasi')
        self.assertContains(verified_response, 'href="https://ppl-m1-fe.vercel.app/"')
        self.assertContains(verified_response, 'Login ke Akun')
        self.assertNotContains(verified_response, 'sedang menunggu verifikasi admin')

        store_response = self.client.get(reverse('partner_ui:my-store'))
        self.assertEqual(store_response.status_code, 200)
        self.assertTemplateUsed(store_response, 'partners/registration_status.html')
        self.assertContains(store_response, 'Pendaftaran Partner')
        self.assertContains(store_response, 'Status pendaftaran')
        self.assertContains(store_response, 'Toko UI Test')
        self.assertContains(store_response, 'Kategori usaha')
        self.assertContains(store_response, 'Tanggal pengajuan')
        self.assertContains(store_response, 'Terverifikasi')
        self.assertNotContains(store_response, 'Pendaftaran partner</a>')

    def test_pending_application_cannot_reopen_or_resubmit_registration(self):
        partner = Partner.objects.create(
            nama_usaha='Usaha Pending',
            kategori_usaha='Produk',
            deskripsi_usaha='Usaha yang menunggu verifikasi.',
            alamat_usaha='Jl. Merdeka No. 1',
            nomor_telepon_usaha='081234567891',
            email_usaha='usaha.pending.lock@example.com',
            status=Partner.StatusPendaftaran.PENDING,
        )
        session = self.client.session
        session['partner_application_id'] = partner.pk
        session.save()

        get_response = self.client.get(self.form_url)
        self.assertRedirects(get_response, reverse('partner_ui:registration-status'))

        post_response = self.client.post(self.form_url, self.valid_payload)
        self.assertRedirects(post_response, reverse('partner_ui:registration-status'))
        self.assertEqual(Partner.objects.count(), 1)

        status_response = self.client.get(reverse('partner_ui:registration-status'))
        self.assertContains(status_response, 'data-registration-status="pending"')
        self.assertContains(status_response, '<span>Toko saya</span>', html=True)
        self.assertNotContains(status_response, '<a href="/toko-saya/">Toko saya</a>', html=True)

    def test_completed_registration_form_saves_documents_and_account(self):
        response = self.client.post(self.form_url, {
            **self.valid_payload,
            'complete_registration': 'true',
            'nama_lengkap': 'Siti Aminah',
            'nik': '3201010101010001',
            'tempat_lahir': 'Bandung',
            'tanggal_lahir': '1995-04-12',
            'ktp': SimpleUploadedFile('ktp.pdf', b'%PDF-1.4 ktp', content_type='application/pdf'),
            'foto_pemegang_ktp': SimpleUploadedFile(
                'pemegang-ktp.pdf',
                b'%PDF-1.4 photo',
                content_type='application/pdf',
            ),
            'account_email': 'siti.ui@example.com',
            'password': 'S3cure!LongPassword-2026',
            'confirm_password': 'S3cure!LongPassword-2026',
        })

        self.assertRedirects(response, reverse('partner_ui:registration-status'))
        partner = Partner.objects.get(email_usaha=self.valid_payload['email_usaha'])
        self.addCleanup(partner.ktp.delete, save=False)
        self.addCleanup(partner.foto_pemegang_ktp.delete, save=False)
        self.assertEqual(partner.nama_lengkap, 'Siti Aminah')
        self.assertEqual(partner.user.email, 'siti.ui@example.com')

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

    def test_t11_ui_shows_rejection_reason_when_ditolak(self):
        partner = Partner.objects.create(
            nama_usaha='Toko Ditolak UI',
            kategori_usaha='Jasa',
            deskripsi_usaha='Layanan.',
            alamat_usaha='Jl. Merdeka No. 3',
            nomor_telepon_usaha='081234567899',
            email_usaha='ditolak_ui@example.com',
            status=Partner.StatusPendaftaran.DITOLAK,
            alasan_penolakan='Dokumen legalitas tidak lengkap.'
        )
        session = self.client.session
        session['partner_application_id'] = partner.pk
        session.save()

        response = self.client.get(reverse('partner_ui:registration-status'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pendaftaran Partner Ditolak')
        self.assertContains(response, 'Alasan penolakan')
        self.assertContains(response, 'Dokumen legalitas tidak lengkap.')
        self.assertContains(response, 'Coba Mendaftar Kembali')
        self.assertContains(response, 'href="/pendaftaran-partner/"')


class PartnerRegistrationTask4_2TestCase(APITestCase):
    def setUp(self):
        self.v1_url = reverse('partners_api:partner-list-create')

    def _generate_dummy_image(self, name='test.png'):
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='blue')
        image.save(file, 'PNG')
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type='image/png')

    def test_post_partner_with_documents_multipart_success(self):
        """
        Task T4.2: Menguji pendaftaran partner multipart dengan Foto KTP,
        Foto Memegang KTP, data NIK, password akun, dan verifikasi kode PRT.
        """
        from django.contrib.auth.hashers import check_password

        ktp_image = self._generate_dummy_image('ktp.png')
        selfie_image = self._generate_dummy_image('selfie_ktp.png')

        payload = {
            "nama_usaha": "Toko Berkah Mandiri",
            "kategori_usaha": "Produk",
            "deskripsi_usaha": "Penyedia sembako dan retail.",
            "alamat_usaha": "Jl. Asia Afrika No. 10, Bandung",
            "nomor_telepon_usaha": "081122334455",
            "email_usaha": "berkah.mandiri@example.com",
            "penanggung_jawab_nama": "Budi Santoso",
            "penanggung_jawab_nik": "3201234567890001",
            "tempat_lahir": "Bandung",
            "tanggal_lahir": "1990-05-15",
            "unit_usaha_id": 1,
            "password": "PasswordAman123!",
            "foto_ktp": ktp_image,
            "foto_memegang_ktp": selfie_image,
        }

        response = self.client.post(self.v1_url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

        data = response.data['data']
        self.assertIn('partner_id', data)
        self.assertTrue(data['partner_id'].startswith('PRT-'))
        self.assertEqual(data['status'], 'pending')
        self.assertEqual(data['penanggung_jawab_nama'], "Budi Santoso")
        self.assertEqual(data['penanggung_jawab_nik'], "3201234567890001")
        self.assertIn('partner_documents/ktp/', data['foto_ktp'])
        self.assertIn('partner_documents/selfie/', data['foto_memegang_ktp'])

        # Pastikan password dan password_hash tidak bocor pada response JSON
        self.assertNotIn('password', data)
        self.assertNotIn('password_hash', data)

        # Verifikasi di database
        partner = Partner.objects.get(email_usaha="berkah.mandiri@example.com")
        self.assertEqual(partner.partner_id, data['partner_id'])
        self.assertTrue(partner.partner_id.startswith('PRT-'))
        self.assertEqual(partner.status, Partner.StatusPendaftaran.PENDING)
        self.assertTrue(check_password("PasswordAman123!", partner.password_hash))

    def test_lookup_status_by_partner_id_string(self):
        """
        Task T4.2: Memastikan endpoint GET detail mendukung pencarian melalui
        kode unik string partner_id (PRT-...).
        """
        partner = Partner.objects.create(
            nama_usaha="Toko String Lookup",
            kategori_usaha="Jasa",
            deskripsi_usaha="Layanan perbaikan.",
            alamat_usaha="Jl. Riau No. 12",
            nomor_telepon_usaha="089988776655",
            email_usaha="lookup@example.com",
            status=Partner.StatusPendaftaran.PENDING
        )
        self.assertTrue(partner.partner_id.startswith('PRT-'))

        url = reverse('partners_api:partner-detail-by-partner-id', kwargs={'identifier': partner.partner_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['partner_id'], partner.partner_id)
        self.assertEqual(response.data['data']['nama_usaha'], "Toko String Lookup")


class PartnerValidationTask5_2TestCase(APITestCase):
    """
    Rangkaian pengujian Task T5.2:
    Validasi Backend untuk NIK 16 Digit, Format Berkas Foto Dokumen (JPG/PNG maks 5MB),
    dan Password Kuat (minimal 8 karakter kombinasi huruf & angka).
    """

    def setUp(self):
        self.v1_url = reverse('partners_api:partner-list-create')
        self.base_payload = {
            "nama_usaha": "Usaha Uji Validasi",
            "kategori_usaha": "Produk",
            "deskripsi_usaha": "Deskripsi pengujian validasi backend.",
            "alamat_usaha": "Jl. Setiabudi No. 100, Bandung",
            "nomor_telepon_usaha": "081234567890",
            "email_usaha": "validasi.t52@example.com",
            "penanggung_jawab_nama": "Moch Hary",
        }

    def _generate_dummy_image(self, name='test.png'):
        file = io.BytesIO()
        image = Image.new('RGB', (50, 50), color='green')
        image.save(file, 'PNG')
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type='image/png')

    def _generate_oversized_image(self, name='large.png'):
        import os
        img = Image.frombytes('RGB', (1400, 1400), os.urandom(1400 * 1400 * 3))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return SimpleUploadedFile(name, buf.read(), content_type='image/png')

    def test_nik_under_16_digits_rejected(self):
        """NIK kurang dari 16 digit harus ditolak dengan error 422 VALIDATION_ERROR."""
        payload = self.base_payload.copy()
        payload["penanggung_jawab_nik"] = "123456789012345"  # 15 digit
        response = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
        self.assertIn('penanggung_jawab_nik', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['penanggung_jawab_nik'],
            "NIK penanggung jawab harus tepat 16 digit angka."
        )

    def test_nik_over_16_digits_rejected(self):
        """NIK lebih dari 16 digit harus ditolak dengan error 422 VALIDATION_ERROR."""
        payload = self.base_payload.copy()
        payload["penanggung_jawab_nik"] = "12345678901234567"  # 17 digit
        response = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
        self.assertIn('penanggung_jawab_nik', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['penanggung_jawab_nik'],
            "NIK penanggung jawab harus tepat 16 digit angka."
        )

    def test_nik_with_alphabet_rejected(self):
        """NIK berisi karakter huruf harus ditolak dengan error 422 VALIDATION_ERROR."""
        payload = self.base_payload.copy()
        payload["penanggung_jawab_nik"] = "320123456789000A"  # 16 karakter namun ada huruf
        response = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
        self.assertIn('penanggung_jawab_nik', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['penanggung_jawab_nik'],
            "NIK penanggung jawab harus tepat 16 digit angka."
        )

    def test_nik_valid_16_digits_accepted(self):
        """NIK tepat 16 digit angka harus diterima (201 Created)."""
        payload = self.base_payload.copy()
        payload["email_usaha"] = "nik.valid@example.com"
        payload["penanggung_jawab_nik"] = "3201234567890001"
        response = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['penanggung_jawab_nik'], "3201234567890001")

    def test_foto_ktp_invalid_format_rejected(self):
        """Berkas foto KTP berupa dokumen teks/non-gambar harus ditolak dengan error 422."""
        txt_file = SimpleUploadedFile("ktp.txt", b"Bukan gambar KTP", content_type="text/plain")
        payload = self.base_payload.copy()
        payload["email_usaha"] = "ktp.invalid@example.com"
        payload["foto_ktp"] = txt_file

        response = self.client.post(self.v1_url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
        self.assertIn('foto_ktp', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['foto_ktp'],
            "Format berkas foto KTP harus berupa gambar JPG atau PNG."
        )

    def test_foto_ktp_size_exceeds_5mb_rejected(self):
        """Berkas foto KTP dengan ukuran melebihi 5 MB harus ditolak dengan error 422."""
        img_file = self._generate_oversized_image("ktp_large.png")

        payload = self.base_payload.copy()
        payload["email_usaha"] = "ktp.large@example.com"
        payload["foto_ktp"] = img_file

        response = self.client.post(self.v1_url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
        self.assertIn('foto_ktp', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['foto_ktp'],
            "Ukuran berkas foto KTP maksimal 5 MB."
        )

    def test_foto_memegang_ktp_invalid_format_and_oversized_rejected(self):
        """Berkas foto memegang KTP non-gambar dan melebihi 5MB harus ditolak dengan error 422."""
        # Test format bukan gambar
        txt_file = SimpleUploadedFile("selfie.pdf", b"%PDF-1.4...", content_type="application/pdf")
        payload = self.base_payload.copy()
        payload["email_usaha"] = "selfie.invalid@example.com"
        payload["foto_memegang_ktp"] = txt_file

        response = self.client.post(self.v1_url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('foto_memegang_ktp', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['foto_memegang_ktp'],
            "Format berkas foto selfie KTP harus berupa gambar JPG atau PNG."
        )

        # Test ukuran melebihi 5MB
        oversized = self._generate_oversized_image("selfie_large.png")
        payload2 = self.base_payload.copy()
        payload2["email_usaha"] = "selfie.large@example.com"
        payload2["foto_memegang_ktp"] = oversized

        response2 = self.client.post(self.v1_url, data=payload2, format='multipart')
        self.assertEqual(response2.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('foto_memegang_ktp', response2.data['error']['fields'])
        self.assertEqual(
            response2.data['error']['fields']['foto_memegang_ktp'],
            "Ukuran berkas foto selfie KTP maksimal 5 MB."
        )

    def test_password_less_than_8_chars_rejected(self):
        """Password kurang dari 8 karakter harus ditolak dengan error 422."""
        payload = self.base_payload.copy()
        payload["email_usaha"] = "pass.short@example.com"
        payload["password"] = "Pass1"  # 5 karakter

        response = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('password', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['password'],
            "Password minimal 8 karakter dan mengandung kombinasi huruf serta angka."
        )

    def test_password_only_letters_rejected(self):
        """Password hanya huruf tanpa angka harus ditolak dengan error 422."""
        payload = self.base_payload.copy()
        payload["email_usaha"] = "pass.letters@example.com"
        payload["password"] = "HanyaHurufSaja"

        response = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('password', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['password'],
            "Password minimal 8 karakter dan mengandung kombinasi huruf serta angka."
        )

    def test_password_only_numbers_rejected(self):
        """Password hanya angka tanpa huruf harus ditolak dengan error 422."""
        payload = self.base_payload.copy()
        payload["email_usaha"] = "pass.numbers@example.com"
        payload["password"] = "1234567890"

        response = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('password', response.data['error']['fields'])
        self.assertEqual(
            response.data['error']['fields']['password'],
            "Password minimal 8 karakter dan mengandung kombinasi huruf serta angka."
        )

    def test_password_strong_accepted(self):
        """Password kuat kombinasi huruf dan angka >= 8 karakter harus diterima."""
        from django.contrib.auth.hashers import check_password

        payload = self.base_payload.copy()
        payload["email_usaha"] = "pass.strong@example.com"
        payload["password"] = "ArayaPartner2026"

        response = self.client.post(self.v1_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        partner = Partner.objects.get(email_usaha="pass.strong@example.com")
        self.assertTrue(check_password("ArayaPartner2026", partner.password_hash))
