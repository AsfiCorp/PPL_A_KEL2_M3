from django.urls import path
from . import views

app_name = 'partners_api'

urlpatterns = [
    path('', views.PartnerListCreateView.as_view(), name='partner-list-create'),
    path('<int:pk>/', views.PartnerDetailView.as_view(), name='partner-detail'),
    path('<str:identifier>/', views.PartnerDetailView.as_view(), name='partner-detail-by-partner-id'),
]
