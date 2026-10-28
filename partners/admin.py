from django.contrib import admin
from .models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_usaha', 'kategori_usaha', 'email_usaha', 'status', 'created_at')
    list_filter = ('status', 'kategori_usaha', 'created_at')
    search_fields = ('nama_usaha', 'email_usaha', 'nomor_telepon_usaha')
    readonly_fields = ('created_at', 'updated_at')
