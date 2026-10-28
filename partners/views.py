from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import PartnerRegistrationSerializer


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
