from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.hashers import make_password
from .models import Partner
from .validators import validate_nik, validate_image_document, validate_strong_password


class PartnerRegistrationSerializer(serializers.ModelSerializer):
    partner_id = serializers.CharField(read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        allow_null=True
    )
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
    penanggung_jawab_nik = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    foto_ktp = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid_image': 'Format berkas foto KTP harus berupa gambar JPG atau PNG.',
        }
    )
    foto_memegang_ktp = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid_image': 'Format berkas foto selfie KTP harus berupa gambar JPG atau PNG.',
        }
    )
    profil_usaha = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid_image': 'Format berkas profil usaha harus berupa gambar JPG atau PNG.',
        }
    )
    rejection_reason = serializers.CharField(
        source='alasan_penolakan',
        read_only=True,
        allow_null=True
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
            'tempat_lahir',
            'tanggal_lahir',
            'foto_ktp',
            'foto_memegang_ktp',
            'password',
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
        # Logika backend rejection_reason (Task T11):
        # Alasan penolakan hanya aktif bila status bernilai 'ditolak'.
        if instance.status == Partner.StatusPendaftaran.DITOLAK:
            reason = instance.alasan_penolakan or "Pendaftaran ditolak oleh administrator."
            data['alasan_penolakan'] = reason
            data['rejection_reason'] = reason
        else:
            data['alasan_penolakan'] = None
            data['rejection_reason'] = None
        return data

    def validate_email_usaha(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError('Format email tidak valid.')

        normalized_email = value.lower()

        partner_pk = self.instance.pk if self.instance else None
        duplicate_qs = Partner.objects.filter(email_usaha__iexact=normalized_email)
        if partner_pk:
            duplicate_qs = duplicate_qs.exclude(pk=partner_pk)

        if duplicate_qs.exists():
            raise serializers.ValidationError('Email sudah terdaftar.')

        return normalized_email

    def validate_penanggung_jawab_nik(self, value):
        if value is None or str(value).strip() == '':
            return value
        return validate_nik(value)

    def validate_foto_ktp(self, value):
        if not value:
            return value
        return validate_image_document(value, field_label="foto KTP", max_size_mb=5)

    def validate_foto_memegang_ktp(self, value):
        if not value:
            return value
        return validate_image_document(value, field_label="foto selfie KTP", max_size_mb=5)

    def validate_profil_usaha(self, value):
        if not value:
            return value
        return validate_image_document(value, field_label="profil usaha", max_size_mb=5)

    def validate_password(self, value):
        if value is None or str(value).strip() == '':
            return value
        return validate_strong_password(value)

    def create(self, validated_data):
        validated_data['status'] = Partner.StatusPendaftaran.PENDING

        password = validated_data.pop('password', None)
        if password:
            validated_data['password_hash'] = make_password(password)

        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user

        return super().create(validated_data)
