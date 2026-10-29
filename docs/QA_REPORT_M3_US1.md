# 📋 QA Acceptance Testing & Code Review Report: M3-US1 (Pendaftaran Partner)

- **Task Linear:** [PRO-29] T7: Pengujian fungsional seluruh AC M3-US1 & code review
- **Parent Story:** [PRO-5] M3-US1: Pendaftaran Partner
- **Sprint / Cycle:** Cycle 1 (25 Okt – 22 Nov 2026)
- **Tester (QA):** Athaillah SulthanFI (`athaillahsfi@gmail.com`)
- **Tanggal Pengujian:** 29 Oktober 2026
- **Target Endpoint:** `POST /api/partners/register/`

---

## 1. Ringkasan Eksekutif

Pengujian fungsional otomatis terhadap seluruh **Acceptance Criteria (AC)** pada User Story `M3-US1: Pendaftaran Partner` telah selesai dilakukan menggunakan Django Test Framework + Django REST Framework APIClient.

Test suite QA tersimpan di: `partners/tests_qa.py`.

### Matriks Hasil Pengujian Acceptance Criteria

| No | Acceptance Criteria (Linear PRO-5) | Expected Result | Status di `main` | Status di `feature/PRO-27` (T5) | Catatan QA |
|---|---|---|---|---|---|
| **AC 1** | Partner isi form pendaftaran lengkap, submit | HTTP 201 Created, status `"pending"`, data tersimpan di DB | ✅ **PASS** | ✅ **PASS** | Model default & serializer create method berfungsi sesuai kontrak. |
| **AC 2** | Partner isi form tidak lengkap, submit | HTTP 400 Bad Request, menampilkan daftar field yang kurang | ✅ **PASS** | ✅ **PASS** | T5 sudah menambahkan custom error messages bahasa Indonesia untuk semua field wajib. |
| **AC 3** | Email sudah terdaftar, submit | HTTP 400 Bad Request, pesan: *"Email sudah terdaftar"* | ⚠️ **PARTIAL** | ⚠️ **PARTIAL (BUG)** | 400 terlempar karena `unique=True` di model, **tetapi pesannya masih default DRF**: `"Partner with this email usaha already exists."` (belum dilokalkan sesuai AC). |
| **AC 4** | Format email tidak valid, submit | HTTP 400 Bad Request, pesan: *"Format email tidak valid"* | ⚠️ **PARTIAL** | ✅ **PASS** | T5 menambahkan `validate_email_usaha` yang melempar pesan *"Format email tidak valid."* |

---

## 2. Edge Cases Tambahan yang Diuji QA

| Kasus Uji | Skenario | Hasil |
|---|---|---|
| **Edge-01** | `kategori_usaha` diisi nilai di luar choice ('Produk'/'Jasa'), misal: `'Fintech'` | ✅ **PASS** (HTTP 400 Bad Request dengan invalid_choice error) |
| **Edge-02** | HTTP Method selain POST (misal: `GET /api/partners/register/`) | ✅ **PASS** (HTTP 405 Method Not Allowed) |
| **Edge-03** | Registrasi dengan file gambar valid (PNG/JPG) | ✅ **PASS** (HTTP 201 Created, `profil_usaha` tersimpan di media) |
| **Edge-04** | Pendaftaran oleh User terotentikasi | ✅ **PASS** (Foreign Key `user` terhubung ke instance auth) |

---

## 3. Temuan Penting & Panduan untuk Developer (Action Items)

### 🔴 Action Item 1 (Untuk Mochammad Hari – Backend / Task T5 / GitHub Issue #3):
**Perbaiki Pesan Validasi Duplikasi Email (AC 3)**
Pada branch `feature/PRO-27-T5-validasi-backend`, file `partners/serializers.py`:

```python
# Tambahkan import validator di bagian atas:
from rest_framework.validators import UniqueValidator

# Pada serializer field email_usaha, tambahkan UniqueValidator:
class PartnerRegistrationSerializer(serializers.ModelSerializer):
    email_usaha = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Partner.objects.all(),
                message='Email sudah terdaftar.'  # <-- WAJIB SESUAI AC 3
            )
        ],
        error_messages={
            'blank': 'Email usaha wajib diisi.',
            'required': 'Email usaha wajib diisi.',
            'invalid': 'Format email tidak valid.',
        }
    )
```

### 🟡 Action Item 2 (Untuk Dokumentasi / Seluruh Tim):
**Inkonsistensi README vs Model (SVG File)**
- Pada `README.md` tertulis field `profil_usaha` mendukung: *"File PNG, JPG, atau SVG"*.
- Namun model menggunakan `models.ImageField` yang didukung `Pillow`. Pillow **tidak bisa membaca format file SVG** (SVG adalah berkas vektor XML, bukan raster image), sehingga upload SVG akan menghasilkan error 400 invalid image.
- **Rekomendasi QA:** Update README untuk hanya mencantumkan PNG dan JPG/JPEG, kecuali jika tim memutuskan migrasi ke `FileField` dengan sanitizer XML khusus untuk mencegah Stored XSS via SVG.

---

## 4. Cara Menjalankan Automated Test Suite QA

```powershell
# Di root direktori project (C:\PPL_A_KEL2_M3)
.\venv\Scripts\python.exe manage.py test partners.tests_qa -v 2
```

Hasil eksekusi:
```text
Found 6 test(s).
test_ac1_form_lengkap_status_pending (partners.tests_qa.TestM3US1AcceptanceCriteria.test_ac1_form_lengkap_status_pending) ... ok
test_ac2_form_tidak_lengkap_ditolak (partners.tests_qa.TestM3US1AcceptanceCriteria.test_ac2_form_tidak_lengkap_ditolak) ... ok
test_ac3_email_duplikat_ditolak_dengan_pesan_spesifik (partners.tests_qa.TestM3US1AcceptanceCriteria.test_ac3_email_duplikat_ditolak_dengan_pesan_spesifik) ... ok
test_ac4_format_email_invalid (partners.tests_qa.TestM3US1AcceptanceCriteria.test_ac4_format_email_invalid) ... ok
test_edge_kategori_usaha_invalid (partners.tests_qa.TestM3US1AcceptanceCriteria.test_edge_kategori_usaha_invalid) ... ok
test_method_not_allowed_on_get (partners.tests_qa.TestM3US1AcceptanceCriteria.test_method_not_allowed_on_get) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.057s

OK
```
