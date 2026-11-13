from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
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
    has_applications = partners.exists()
    query = request.GET.get('q', '').strip()
    if has_applications and not query:
        partner = partners.first()
        return render(
            request,
            'partners/registration_status.html',
            {
                'active_page': 'my_store',
                'partner': partner,
                'submitted_at': timezone.localtime(partner.created_at),
            },
        )
    if query:
        partners = partners.filter(nama_usaha__icontains=query)
    return render(
        request,
        'partners/my_store.html',
        {
            'active_page': 'my_store',
            'partners': partners,
            'has_applications': has_applications,
            'query': query,
        },
    )


@never_cache
def register_partner(request):
    application_id = request.session.get('partner_application_id')
    if application_id and Partner.objects.filter(
        pk=application_id,
        status=Partner.StatusPendaftaran.PENDING,
    ).exists():
        return redirect('partner_ui:registration-status')

    if request.method == 'POST':
        if request.POST.get('complete_registration') == 'true':
            registration_data = request.POST.copy()
            registration_data.update(request.FILES)
            serializer = PartnerRegistrationSerializer(
                data=registration_data,
                context={'request': request},
            )
            if serializer.is_valid():
                partner = serializer.save()
                request.session['partner_application_id'] = partner.pk
                messages.success(request, 'Pendaftaran partner berhasil dikirim.')
                return redirect('partner_ui:registration-status')

            form = PartnerRegistrationForm(request.POST, request.FILES)
            return render(
                request,
                'partners/register_partner.html',
                {
                    'active_page': 'my_store',
                    'form': form,
                    'registration_errors': serializer.errors,
                },
            )

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


@never_cache
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


def openapi_yaml(request):
    openapi_file = settings.BASE_DIR / 'docs' / 'openapi.yaml'
    if not openapi_file.exists():
        raise Http404('File docs/openapi.yaml tidak ditemukan.')
    return HttpResponse(openapi_file.read_text(encoding='utf-8'), content_type='text/yaml')


def api_docs(request):
    html_content = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="utf-8" />
  <title>Dokumentasi API Modul M3 - Araya Business Hub</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  <style>
    body { margin: 0; background: #fafafa; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => {
      window.ui = SwaggerUIBundle({
        url: '/api/m3/v1/openapi.yaml',
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
      });
    };
  </script>
</body>
</html>"""
    return HttpResponse(html_content, content_type='text/html')


class PartnerListCreateView(APIView):
    """
    Endpoint Modul 3:
    POST /api/m3/v1/partners -> Pendaftaran partner baru (M3-US1).
    GET  /api/m3/v1/partners -> Daftar partner terverifikasi untuk katalog M5 (K-06).
    """
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        status_filter = request.GET.get('status', 'terverifikasi').strip()
        queryset = Partner.objects.all()
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        search_query = request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(nama_usaha__icontains=search_query)

        try:
            page = max(1, int(request.GET.get('page', 1)))
        except ValueError:
            page = 1

        try:
            per_page = min(100, max(1, int(request.GET.get('per_page', 20))))
        except ValueError:
            per_page = 20

        total = queryset.count()
        start = (page - 1) * per_page
        end = start + per_page
        records = queryset[start:end]

        serializer = PartnerRegistrationSerializer(records, many=True)
        total_pages = (total + per_page - 1) // per_page if total > 0 else 1

        return Response(
            {
                "success": True,
                "data": serializer.data,
                "meta": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "total_pages": total_pages,
                }
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = PartnerRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            partner = serializer.save()
            request.session['partner_application_id'] = partner.pk
            return Response(
                {
                    "success": True,
                    "status": "success",
                    "message": "Pendaftaran partner berhasil dikirim dan menunggu verifikasi.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        raw_errors = serializer.errors
        fields_error = {}
        for key, errs in raw_errors.items():
            if isinstance(errs, list) and len(errs) > 0:
                fields_error[key] = str(errs[0])
            else:
                fields_error[key] = str(errs)

        # Analisis kode galat sesuai Panduan API Bersama
        email_errors = raw_errors.get('email_usaha', [])
        email_err_str = ' '.join(str(e) for e in email_errors).lower()

        if 'sudah terdaftar' in email_err_str or 'already exists' in email_err_str:
            error_code = 'EMAIL_DUPLICATE'
            message = 'Email sudah terdaftar.'
            http_status = status.HTTP_409_CONFLICT
        elif 'tidak valid' in email_err_str or 'valid email' in email_err_str:
            error_code = 'EMAIL_INVALID'
            message = 'Format email tidak valid.'
            http_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            error_code = 'VALIDATION_ERROR'
            message = 'Isian tidak lolos validasi. Periksa kelengkapan data.'
            http_status = status.HTTP_422_UNPROCESSABLE_ENTITY

        return Response(
            {
                "success": False,
                "status": "error",
                "message": message,
                "error": {
                    "code": error_code,
                    "message": message,
                    "fields": fields_error
                },
                "errors": fields_error
            },
            status=http_status
        )


class PartnerDetailView(APIView):
    """
    Endpoint Modul 3:
    GET /api/m3/v1/partners/{id} atau {partner_id} -> Detail dan status pendaftaran partner (M3-US3).
    """
    def get(self, request, pk=None, identifier=None, *args, **kwargs):
        val = pk if pk is not None else identifier
        partner = None
        if val is not None:
            if str(val).isdigit():
                partner = Partner.objects.filter(pk=int(val)).first()
            if not partner:
                partner = Partner.objects.filter(partner_id__iexact=str(val)).first()

        if not partner:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "PARTNER_NOT_FOUND",
                        "message": "Data partner tidak ditemukan.",
                        "fields": None
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PartnerRegistrationSerializer(partner, context={'request': request})
        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class PartnerRegistrationView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = PartnerRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            partner = serializer.save()
            request.session['partner_application_id'] = partner.pk
            return Response(
                {
                    'status': 'success',
                    'message': 'Pendaftaran partner berhasil dikirim dan menunggu verifikasi.',
                    'data': serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                'status': 'error',
                'message': 'Pendaftaran gagal. Silakan periksa kembali data yang diisi.',
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
