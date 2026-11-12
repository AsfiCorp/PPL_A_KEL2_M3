import re
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import FileExtensionValidator, validate_email
from django.db import transaction
from rest_framework import serializers

from .models import Partner
from .validators import validate_image_document, validate_nik, validate_strong_password

User = get_user_model()


class PartnerRegistrationSerializer(serializers.ModelSerializer):
    partner_id = serializers.CharField(read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=False,
    )
    email_usaha = serializers.EmailField(
        validators=[],
        error_messages={
            'blank': 'Email usaha wajib diisi.',
            'required': 'Email usaha wajib diisi.',
            'invalid': 'Format email tidak valid.',
        },
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        trim_whitespace=False,
    )
    account_email = serializers.EmailField(required=False, allow_blank=True, write_only=True)
    complete_registration = serializers.BooleanField(required=False, default=False, write_only=True)
    nama_lengkap = serializers.CharField(required=False, allow_blank=True, max_length=255)
    nik = serializers.CharField(required=False, allow_blank=True, max_length=16)
    ktp = serializers.FileField(
        required=False,
        allow_null=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'pdf'])],
    )
    foto_pemegang_ktp = serializers.FileField(
        required=False,
        allow_null=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'pdf'])],
    )
    penanggung_jawab_nik = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    foto_ktp = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={'invalid_image': 'Format berkas foto KTP harus berupa gambar JPG atau PNG.'},
    )
    foto_memegang_ktp = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={'invalid_image': 'Format berkas foto selfie KTP harus berupa gambar JPG atau PNG.'},
    )
    profil_usaha = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={'invalid_image': 'Format berkas profil usaha harus berupa gambar JPG atau PNG.'},
    )
    rejection_reason = serializers.CharField(
        source='alasan_penolakan',
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Partner
        fields = [
            'id',
            'partner_id',
            'unit_usaha_id',
            'nama_usaha',
            'kategori_usaha',
            'deskripsi_usaha',
            'alamat_usaha',
            'nomor_telepon_usaha',
            'email_usaha',
            'profil_usaha',
            'penanggung_jawab_nama',
            'penanggung_jawab_nik',
            'nama_lengkap',
            'nik',
            'tempat_lahir',
            'tanggal_lahir',
            'foto_ktp',
            'foto_memegang_ktp',
            'ktp',
            'foto_pemegang_ktp',
            'complete_registration',
            'account_email',
            'password',
            'confirm_password',
            'status',
            'alasan_penolakan',
            'rejection_reason',
            'alasan_penangguhan',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'partner_id',
            'status',
            'alasan_penolakan',
            'rejection_reason',
            'alasan_penangguhan',
            'created_at',
            'updated_at',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.status == Partner.StatusPendaftaran.DITOLAK:
            reason = instance.alasan_penolakan or 'Pendaftaran ditolak oleh administrator.'
            data['alasan_penolakan'] = reason
            data['rejection_reason'] = reason
        else:
            data['alasan_penolakan'] = None
            data['rejection_reason'] = None
        return data

    def validate_email_usaha(self, value):
        try:
            validate_email(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError('Format email tidak valid.') from exc

        normalized_email = value.lower()
        duplicate_qs = Partner.objects.filter(email_usaha__iexact=normalized_email)
        if self.instance:
            duplicate_qs = duplicate_qs.exclude(pk=self.instance.pk)
        if duplicate_qs.exists():
            raise serializers.ValidationError('Email sudah terdaftar.')
        return normalized_email

    def validate_penanggung_jawab_nik(self, value):
        if value is None or not str(value).strip():
            return value
        return validate_nik(value)

    def validate_nik(self, value):
        if value:
            return validate_nik(value)
        return value

    def validate_foto_ktp(self, value):
        if value:
            return validate_image_document(value, field_label='foto KTP', max_size_mb=5)
        return value

    def validate_foto_memegang_ktp(self, value):
        if value:
            return validate_image_document(value, field_label='foto selfie KTP', max_size_mb=5)
        return value

    def validate_profil_usaha(self, value):
        if value:
            return validate_image_document(value, field_label='profil usaha', max_size_mb=5)
        return value

    def validate_ktp(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Ukuran dokumen melebihi 5 MB.')
        return value

    def validate_foto_pemegang_ktp(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Ukuran dokumen melebihi 5 MB.')
        return value

    def validate_password(self, value):
        if value:
            return validate_strong_password(value)
        return value

    def validate(self, attrs):
        if attrs.get('complete_registration'):
            required_fields = (
                'nama_lengkap',
                'nik',
                'tempat_lahir',
                'tanggal_lahir',
                'ktp',
                'foto_pemegang_ktp',
                'account_email',
                'password',
                'confirm_password',
            )
            errors = {
                field: ['Bagian ini wajib diisi.']
                for field in required_fields
                if not attrs.get(field)
            }
            if errors:
                raise serializers.ValidationError(errors)

        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password and confirm_password is not None and confirm_password != password:
            raise serializers.ValidationError({
                'confirm_password': ['Konfirmasi password tidak cocok.'],
            })

        email = attrs.get('account_email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({
                'account_email': ['Email ini sudah digunakan.'],
            })

        if attrs.get('nama_lengkap'):
            attrs.setdefault('penanggung_jawab_nama', attrs['nama_lengkap'])
        if attrs.get('nik'):
            attrs.setdefault('penanggung_jawab_nik', attrs['nik'])
        if attrs.get('ktp'):
            attrs.setdefault('foto_ktp', attrs['ktp'])
        if attrs.get('foto_pemegang_ktp'):
            attrs.setdefault('foto_memegang_ktp', attrs['foto_pemegang_ktp'])
        if attrs.get('penanggung_jawab_nama'):
            attrs.setdefault('nama_lengkap', attrs['penanggung_jawab_nama'])
        if attrs.get('penanggung_jawab_nik'):
            attrs.setdefault('nik', attrs['penanggung_jawab_nik'])

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('complete_registration', None)
        account_email = validated_data.pop('account_email', '')
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        validated_data['status'] = Partner.StatusPendaftaran.PENDING

        if password:
            validated_data['password_hash'] = make_password(password)

        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user
        elif account_email and password:
            validated_data['user'] = User.objects.create_user(
                username=f'partner_{uuid4().hex}',
                email=account_email,
                first_name=validated_data.get('nama_lengkap', ''),
                password=password,
            )

        return super().create(validated_data)
