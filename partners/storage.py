import os
import urllib.request
import urllib.error
import urllib.parse
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class SupabaseStorage(FileSystemStorage):
    """
    Storage backend yang menyimpan berkas ke Supabase Cloud Storage
    bila konfigurasi SUPABASE_ANON_KEY tersedia.
    Jika tidak tersedia (misal saat automated test lokal tanpa koneksi),
    secara otomatis beralih ke FileSystemStorage lokal.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supabase_url = os.environ.get('SUPABASE_URL', 'https://ahemuctnwslwikbqyyrv.supabase.co').rstrip('/')
        self.supabase_anon_key = os.environ.get('SUPABASE_ANON_KEY', '')
        self.bucket = 'partner-documents'

    def _save(self, name, content):
        # Simpan ke storage lokal / tmp
        saved_name = super()._save(name, content)

        if self.supabase_anon_key:
            try:
                content.seek(0)
                file_data = content.read()
                quoted_name = urllib.parse.quote(saved_name, safe='/')
                upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket}/{quoted_name}"
                headers = {
                    'apikey': self.supabase_anon_key,
                    'Authorization': f"Bearer {self.supabase_anon_key}",
                    'Content-Type': getattr(content, 'content_type', 'application/octet-stream'),
                    'x-upsert': 'true'
                }
                req = urllib.request.Request(upload_url, data=file_data, headers=headers, method='POST')
                with urllib.request.urlopen(req, timeout=15) as resp:
                    pass
            except Exception as e:
                # Jangan biarkan error upload membatalkan transaksi bila lokal tersimpan
                pass

        return saved_name

    def url(self, name):
        if self.supabase_anon_key:
            quoted_name = urllib.parse.quote(name, safe='/')
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{quoted_name}"
        return super().url(name)
