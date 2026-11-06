from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Partner


class PartnerRegistrationSerializer(serializers.ModelSerializer):
    nama_usaha = serializers.CharField(
        max_length=255,
        error_messages={
            'blank': 'Nama usaha wajib diisi.',
            'required': 'Nama usaha wajib diisi.',
        }
    )
    kategori_usaha = serializers.ChoiceField(
        choices=Partner.KategoriUsaha.choices,
        error_messages={
            'blank': 'Kategori usaha wajib diisi.',
            'required': 'Kategori usaha wajib diisi.',
            'invalid_choice': 'Kategori usaha tidak valid.',
        }
    )
    deskripsi_usaha = serializers.CharField(
        error_messages={
            'blank': 'Deskripsi usaha wajib diisi.',
            'required': 'Deskripsi usaha wajib diisi.',
        }
    )
    alamat_usaha = serializers.CharField(
        error_messages={
            'blank': 'Alamat usaha wajib diisi.',
            'required': 'Alamat usaha wajib diisi.',
        }
    )
    nomor_telepon_usaha = serializers.CharField(
        max_length=30,
        error_messages={
            'blank': 'Nomor telepon usaha wajib diisi.',
            'required': 'Nomor telepon usaha wajib diisi.',
        }
    )
    email_usaha = serializers.EmailField(
        error_messages={
            'blank': 'Email usaha wajib diisi.',
            'required': 'Email usaha wajib diisi.',
            'invalid': 'Format email tidak valid.',
        }
    )

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
            'alasan_penolakan',
            'alasan_penangguhan',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'status', 'alasan_penolakan', 'alasan_penangguhan', 'created_at', 'updated_at']

    def validate_email_usaha(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError('Format email tidak valid.')

        normalized_email = value.lower()

        # Validasi keunikan hanya saat create atau perubahan email
        partner_id = self.instance.pk if self.instance else None
        duplicate_qs = Partner.objects.filter(email_usaha__iexact=normalized_email)
        if partner_id:
            duplicate_qs = duplicate_qs.exclude(pk=partner_id)

        if duplicate_qs.exists():
            raise serializers.ValidationError('Email sudah terdaftar.')

        return normalized_email

    def create(self, validated_data):
        validated_data['status'] = Partner.StatusPendaftaran.PENDING

        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user

        return super().create(validated_data)
