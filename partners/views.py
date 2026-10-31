from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .forms import PartnerRegistrationForm
from .models import Partner
from .serializers import PartnerRegistrationSerializer


def home(request):
    return render(request, 'partners/home.html', {'active_page': 'home'})


def my_store(request):
    if request.user.is_authenticated:
        partners = Partner.objects.filter(user=request.user)
    else:
        application_id = request.session.get('partner_application_id')
        partners = Partner.objects.filter(pk=application_id) if application_id else Partner.objects.none()
    query = request.GET.get('q', '').strip()
    if query:
        partners = partners.filter(nama_usaha__icontains=query)
    return render(
        request,
        'partners/my_store.html',
        {'active_page': 'my_store', 'partners': partners, 'query': query},
    )


def register_partner(request):
    if request.method == 'POST':
        form = PartnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            partner = form.save(commit=False)
            if request.user.is_authenticated:
                partner.user = request.user
            partner.save()
            request.session['partner_application_id'] = partner.pk
            messages.success(request, 'Pendaftaran partner berhasil dikirim.')
            return redirect('partner_ui:registration-status')
    else:
        form = PartnerRegistrationForm()

    return render(
        request,
        'partners/register_partner.html',
        {'active_page': 'my_store', 'form': form},
    )


def registration_status(request):
    application_id = request.session.get('partner_application_id')
    if application_id is None:
        return redirect('partner_ui:my-store')

    try:
        partner = Partner.objects.get(pk=application_id)
    except Partner.DoesNotExist:
        request.session.pop('partner_application_id', None)
        return redirect('partner_ui:my-store')
    return render(
        request,
        'partners/registration_status.html',
        {
            'active_page': 'my_store',
            'partner': partner,
            'submitted_at': timezone.localtime(partner.created_at),
        },
    )


class PartnerRegistrationView(APIView):
    """
    API Endpoint untuk pendaftaran calon Partner baru (M3-US1 / Task T4).
    Metode: POST
    Status awal pendaftaran: 'pending' (Menunggu Persetujuan)
    """
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = PartnerRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Pendaftaran partner berhasil dikirim dan menunggu verifikasi.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "status": "error",
                "message": "Pendaftaran gagal. Silakan periksa kembali data yang diisi.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
