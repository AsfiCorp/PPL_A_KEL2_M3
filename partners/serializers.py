from rest_framework import serializers
from .models import Partner


class PartnerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = [
            'id',
            'nama_usaha',
            'kategori_usaha',
            'deskripsi_usaha',
            'alamat_usaha',
            'nomor_telepon_usaha',
            'email_usaha',
            'profil_usaha',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        # Default status for new registration is always pending
        validated_data['status'] = Partner.StatusPendaftaran.PENDING

        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user

        return super().create(validated_data)

