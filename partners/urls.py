from django.urls import path
from .views import PartnerRegistrationView

app_name = 'partners'

urlpatterns = [
    path('register/', PartnerRegistrationView.as_view(), name='partner-register'),
]

