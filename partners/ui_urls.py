from django.urls import path
from . import views

app_name = 'partner_ui'

urlpatterns = [
    path('', views.home, name='home'),
    path('toko-saya/', views.my_store, name='my-store'),
    path('pendaftaran-partner/', views.register_partner, name='partner-registration'),
    path('pendaftaran-partner/status/', views.registration_status, name='registration-status'),
]
