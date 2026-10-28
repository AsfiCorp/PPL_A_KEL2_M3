from django.db import models
from django.conf import settings


class Partner(models.Model):
    class KategoriUsaha(models.TextChoices):
        PRODUK = 'Produk', 'Produk'
        JASA = 'Jasa', 'Jasa'

    class StatusPendaftaran(models.TextChoices):
        PENDING = 'pending', 'Menunggu Persetujuan'
        TERVERIFIKASI = 'terverifikasi', 'Terverifikasi'
        DITOLAK = 'ditolak', 'Ditolak'
        DITANGGUHKAN = 'ditangguhkan', 'Ditangguhkan'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_applications'
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
        ordering = ['-created_at']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return f"{self.nama_usaha} ({self.get_status_display()})"
