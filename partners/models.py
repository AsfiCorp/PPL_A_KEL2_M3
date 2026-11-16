import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


def generate_partner_id():
    date_str = timezone.now().strftime("%Y%m%d")
    unique_suffix = uuid.uuid4().hex[:4].upper()
    return f"PRT-{date_str}-{unique_suffix}"


class Partner(models.Model):
    class KategoriUsaha(models.TextChoices):
        PRODUK = 'Produk', 'Produk'
        JASA = 'Jasa', 'Jasa'

    class StatusPendaftaran(models.TextChoices):
        PENDING = 'pending', 'Menunggu Persetujuan'
        APPROVE = 'approve', 'Disetujui'
        ACTIVE = 'active', 'Aktif'
        REJECT = 'reject', 'Ditolak'
        SUSPEND = 'suspend', 'Ditangguhkan'
        # Alias kompatibilitas
        TERVERIFIKASI = 'terverifikasi', 'Terverifikasi'
        DITOLAK = 'ditolak', 'Ditolak'
        DITANGGUHKAN = 'ditangguhkan', 'Ditangguhkan'

    partner_id = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        null=True,
        blank=True
    )
    unit_usaha_id = models.IntegerField(null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_applications',
        db_constraint=False
    )
    nama_usaha = models.CharField(max_length=255)
    kategori_usaha = models.CharField(
        max_length=50,
        choices=KategoriUsaha.choices
    )
    deskripsi_usaha = models.TextField()
    alamat_usaha = models.TextField()
    nomor_telepon_usaha = models.CharField(max_length=30)
    email_usaha = models.EmailField(unique=True)
    profil_usaha = models.ImageField(
        upload_to='partner_profiles/',
        null=True,
        blank=True
    )
    nama_lengkap = models.CharField(max_length=255, blank=True)
    nik = models.CharField(max_length=16, blank=True)
    tempat_lahir = models.CharField(max_length=100, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    ktp = models.FileField(upload_to='partner_documents/ktp/', null=True, blank=True)
    foto_pemegang_ktp = models.FileField(
        upload_to='partner_documents/ktp_holders/',
        null=True,
        blank=True,
    )

    # Identitas Penanggung Jawab & Dokumen
    penanggung_jawab_nama = models.CharField(max_length=255, null=True, blank=True)
    penanggung_jawab_nik = models.CharField(max_length=16, null=True, blank=True)
    tempat_lahir = models.CharField(max_length=100, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    foto_ktp = models.ImageField(
        upload_to='partner_documents/ktp/',
        null=True,
        blank=True
    )
    foto_memegang_ktp = models.ImageField(
        upload_to='partner_documents/selfie/',
        null=True,
        blank=True
    )

    # Kredensial Akun (Login M1)
    password_hash = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=StatusPendaftaran.choices,
        default=StatusPendaftaran.PENDING
    )
    alasan_penolakan = models.TextField(blank=True, null=True)
    alasan_penangguhan = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'partners'
        ordering = ['-created_at']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        if not is_new:
            orig = Partner.objects.filter(pk=self.pk).values('status').first()
            if orig:
                old_status = orig['status']

        if not self.partner_id:
            while True:
                candidate = generate_partner_id()
                if not Partner.objects.filter(partner_id=candidate).exists():
                    self.partner_id = candidate
                    break

        super().save(*args, **kwargs)

        # Otomatis catat ke riwayat PartnerStatusLog
        if is_new:
            PartnerStatusLog.objects.create(
                partner=self,
                status_sebelum='none',
                status_sesudah=self.status,
                aksi='REGISTRASI_BARU',
                alasan='Pendaftaran partner baru oleh mitra'
            )
        elif old_status and old_status != self.status:
            alasan_text = (
                self.alasan_penolakan if self.status in ['ditolak', 'reject']
                else self.alasan_penangguhan if self.status in ['ditangguhkan', 'suspend']
                else 'Perubahan status pendaftaran oleh sistem/admin'
            )
            PartnerStatusLog.objects.create(
                partner=self,
                status_sebelum=old_status,
                status_sesudah=self.status,
                aksi=f'STATUS_{self.status.upper()}',
                alasan=alasan_text
            )

    def __str__(self):
        return f"{self.nama_usaha} [{self.partner_id}] ({self.get_status_display()})"


class PartnerStatusLog(models.Model):
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='status_logs'
    )
    admin_id = models.BigIntegerField(null=True, blank=True)
    status_sebelum = models.CharField(max_length=20)
    status_sesudah = models.CharField(max_length=20)
    aksi = models.CharField(max_length=50)
    alasan = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'partner_status_logs'
        ordering = ['-created_at']
        verbose_name = 'Partner Status Log'
        verbose_name_plural = 'Partner Status Logs'

    def __str__(self):
        return f"Log #{self.pk} - {self.partner.nama_usaha} ({self.aksi})"
