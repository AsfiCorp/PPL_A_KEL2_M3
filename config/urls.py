"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from partners.views import api_docs, openapi_yaml

urlpatterns = [
    path('admin/', admin.site.urls),
    # Antarmuka Pengguna (UI)
    path('', include('partners.ui_urls')),
    # Standar Panduan API Bersama (Modul M3 v1)
    path('api/m3/v1/partners/', include('partners.api_urls', namespace='partners_api')),
    path('api/m3/v1/docs/', api_docs, name='api-docs'),
    path('api/m3/v1/openapi.yaml', openapi_yaml, name='openapi-yaml'),
    # Kompatibilitas mundur endpoint sebelumnya
    path('api/partners/', include('partners.urls', namespace='partners')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
