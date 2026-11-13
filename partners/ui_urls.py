from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'partner_ui'

urlpatterns = [
    path('', views.home, name='home'),
    path('keluar/', LogoutView.as_view(next_page='partner_ui:home'), name='logout'),
    path('toko-saya/', views.my_store, name='my-store'),
    path('pendaftaran-partner/', views.register_partner, name='partner-registration'),
    path('pendaftaran-partner/status/', views.registration_status, name='registration-status'),
]
