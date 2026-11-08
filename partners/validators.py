import re
from pathlib import Path
from rest_framework import serializers


def validate_nik(value):
    """
    Validasi NIK penanggung jawab:
    Wajib tepat 16 digit angka.
    """
    if value is None:
        return value

    cleaned = str(value).strip()
    if not cleaned:
        raise serializers.ValidationError("NIK penanggung jawab wajib diisi.")

    if not re.match(r'^\d{16}$', cleaned):
        raise serializers.ValidationError("NIK penanggung jawab harus tepat 16 digit angka.")

    return cleaned


def validate_image_document(file_obj, field_label="foto", max_size_mb=5):
    """
    Validasi berkas dokumen unggahan (foto KTP, foto memegang KTP, profil usaha):
    - Format berkas: JPG, JPEG, PNG.
    - Ukuran berkas: Maksimal 5 MB.
    """
    if not file_obj:
        return file_obj

    max_bytes = max_size_mb * 1024 * 1024
    if file_obj.size > max_bytes:
        raise serializers.ValidationError(f"Ukuran berkas {field_label} maksimal {max_size_mb} MB.")

    allowed_extensions = {'.jpg', '.jpeg', '.png'}
    ext = Path(file_obj.name).suffix.lower()
    content_type = getattr(file_obj, 'content_type', '').lower()

    if ext not in allowed_extensions:
        raise serializers.ValidationError(f"Format berkas {field_label} harus berupa gambar JPG atau PNG.")

    if content_type and not (
        content_type in {'image/jpeg', 'image/png', 'image/jpg'}
        or content_type.startswith('image/')
    ):
        raise serializers.ValidationError(f"Format berkas {field_label} harus berupa gambar JPG atau PNG.")

    return file_obj


def validate_strong_password(value):
    """
    Validasi keamanan password akun mitra:
    - Minimal 8 karakter.
    - Mengandung kombinasi huruf (alfabet) dan angka (numerik).
    """
    if value is None:
        return value

    password_str = str(value)
    if len(password_str) < 8 or not re.search(r'[A-Za-z]', password_str) or not re.search(r'\d', password_str):
        raise serializers.ValidationError(
            "Password minimal 8 karakter dan mengandung kombinasi huruf serta angka."
        )

    return value
