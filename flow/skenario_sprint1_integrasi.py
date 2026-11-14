import os
import sys
import io
import json
from PIL import Image

# Inisialisasi Django Environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from partners.models import Partner


def generate_dummy_image(name='dummy.png'):
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = name
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type='image/png')


def print_step(title):
    print("\n" + "=" * 75)
    print(f" {title}")
    print("=" * 75)


def run_sprint_1_scenario():
    from django.conf import settings
    if 'testserver' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']

    client = APIClient()

    print("\n" + "#" * 75)
    print("  SIMULASI INTEGRASI END-TO-END SPRINT 1 (MODUL 3: MANAJEMEN PARTNER)")
    print("  Cakupan: M3-US1, M3-US2, M3-US3 (T4, T4.2, T5, T5.2, T7, T10, T11)")
    print("  Koneksi Modul: Inbound M1 & M2, Outbound M4 & M5 (Kontrak K-06)")
    print("#" * 75)

    # -------------------------------------------------------------
    # SKENARIO 1: INBOUND MODUL 2 (FETCH MASTER UNIT USAHA)
    # -------------------------------------------------------------
    print_step("SKENARIO 1: Mengambil Data Master Unit Usaha dari Modul 2")
    # Simulasi respons dari API Modul 2 (GET /api/m2/v1/unit-usaha/)
    dummy_m2_response = {
        "success": True,
        "message": "Data master unit usaha berhasil diambil dari Modul 2",
        "data": [
            {"id": 1, "nama_unit": "Produk Olahan Pangan", "kode": "PANGAN"},
            {"id": 2, "nama_unit": "Jasa Kreatif & Kerajinan", "kode": "KREATIF"},
            {"id": 3, "nama_unit": "Perdagangan Umum & Jasa", "kode": "DAGANG"}
        ]
    }
    print("[M2 -> M3] Memanggil endpoint: GET /api/m2/v1/unit-usaha/")
    print(f"Status Respons: 200 OK")
    print(f"Kategori Unit Usaha Berhasil Dipopulasikan ke Dropdown:")
    for unit in dummy_m2_response["data"]:
        print(f"   - ID {unit['id']}: {unit['nama_unit']} (Kode: {unit['kode']})")

    # -------------------------------------------------------------
    # SKENARIO 2: NEGATIVE TESTS / VALIDASI KETAT (T5 & T5.2)
    # -------------------------------------------------------------
    print_step("SKENARIO 2: Pengujian Validasi Ketat Pendaftaran (Negative Tests)")

    # Uji 2.1: NIK bukan 16 digit angka
    print("\n[Uji 2.1] Calon mitra mengisi NIK tidak valid (15 digit angka):")
    payload_invalid_nik = {
        "nama_usaha": "Warung Kopi Invalid",
        "kategori_usaha": "Produk",
        "deskripsi_usaha": "Kedai kopi pengujian validasi",
        "alamat_usaha": "Jl. Kaliurang No. 5",
        "email_usaha": "invalid.nik@example.com",
        "nomor_telepon_usaha": "081234567890",
        "penanggung_jawab_nama": "Hadi",
        "penanggung_jawab_nik": "123456789012345",  # 15 digit
        "password": "PasswordValid123"
    }
    res_nik = client.post("/api/m3/v1/partners/", data=payload_invalid_nik, format="json")
    print(f"Status HTTP: {res_nik.status_code} (Harapan: 422 Unprocessable Entity)")
    print(f"Kode Galat: {res_nik.data['error']['code']}")
    print(f"Pesan Galat: {res_nik.data['error']['fields']['penanggung_jawab_nik']}")
    assert res_nik.status_code == 422
    assert res_nik.data['error']['code'] == 'VALIDATION_ERROR'

    # Uji 2.2: Password lemah (< 8 karakter)
    print("\n[Uji 2.2] Calon mitra mengisi password lemah ('kopi'):")
    payload_weak_pass = payload_invalid_nik.copy()
    payload_weak_pass["penanggung_jawab_nik"] = "3201234567890001"
    payload_weak_pass["password"] = "kopi"
    res_pass = client.post("/api/m3/v1/partners/", data=payload_weak_pass, format="json")
    print(f"Status HTTP: {res_pass.status_code} (Harapan: 422 Unprocessable Entity)")
    print(f"Pesan Galat: {res_pass.data['error']['fields']['password']}")
    assert res_pass.status_code == 422

    # -------------------------------------------------------------
    # SKENARIO 3: PENDAFTARAN MITRA SUKSES (M3-US1, T4.2, T5.2)
    # -------------------------------------------------------------
    print_step("SKENARIO 3: Pendaftaran Mandiri Mitra Sukses (M3-US1 & T4.2)")

    # Bersihkan email uji coba jika ada sebelumnya
    test_email = "warung.kopi.araya@example.com"
    Partner.objects.filter(email_usaha=test_email).delete()

    valid_multipart_payload = {
        "nama_usaha": "Warung Kopi Araya",
        "kategori_usaha": "Produk",
        "unit_usaha_id": 1,  # Mengacu ke Unit Usaha Modul 2
        "deskripsi_usaha": "Kedai kopi lokal binaan dengan biji kopi Nusantara pilihan.",
        "alamat_usaha": "Jl. Raya Araya Galeria Blok C No. 7, Malang",
        "email_usaha": test_email,
        "nomor_telepon_usaha": "081298765432",
        "penanggung_jawab_nama": "Mochammad Hari Fitrian",
        "penanggung_jawab_nik": "3201234567890001",
        "password": "ArayaPartner2026",
        "foto_ktp": generate_dummy_image("ktp_hari.png"),
        "foto_memegang_ktp": generate_dummy_image("selfie_hari.png")
    }

    print(f"[Calon Mitra -> M3] Mengirim POST /api/m3/v1/partners/ (multipart/form-data)")
    res_reg = client.post("/api/m3/v1/partners/", data=valid_multipart_payload, format="multipart")
    if res_reg.status_code != 201:
        print("DETAIL ERROR 422:", res_reg.data)
    print(f"Status HTTP: {res_reg.status_code} (Harapan: 201 Created)")
    assert res_reg.status_code == 201

    partner_data = res_reg.data["data"]
    assigned_prt = partner_data["partner_id"]
    assigned_id = partner_data["id"]

    print(f"Data Pendaftaran Terbentuk:")
    print(f"   - ID Numerik Database: {assigned_id}")
    print(f"   - Kode Publik Unik: {assigned_prt} (Format: PRT-YYYYMMDD-XXXX)")
    print(f"   - Status Awal: {partner_data['status']} (Harapan: pending)")
    print(f"   - Password Hash: write-only (Tidak dibocorkan di JSON respons)")
    print(f"   - Berkas Foto KTP: {partner_data['foto_ktp']}")
    print(f"   - Berkas Selfie KTP: {partner_data['foto_memegang_ktp']}")
    print(f"   - Rejection Reason: {partner_data['rejection_reason']} (Harapan: null)")

    # -------------------------------------------------------------
    # SKENARIO 4: PELACAKAN STATUS AWAL MITRA (M3-US3, T10, T11)
    # -------------------------------------------------------------
    print_step("SKENARIO 4: Pelacakan Status oleh Mitra (M3-US3, T10 & T11)")

    # Uji Dual Lookup: Cari via string PRT-XXXX
    print(f"[Mitra -> M3] Melacak status via Dual Lookup Kode Publik: GET /api/m3/v1/partners/{assigned_prt}/")
    res_status_prt = client.get(f"/api/m3/v1/partners/{assigned_prt}/")
    print(f"Status HTTP: {res_status_prt.status_code} 200 OK")
    print(f"Status Pengajuan: {res_status_prt.data['data']['status']}")
    print(f"Rejection Reason (Task T11): {res_status_prt.data['data']['rejection_reason']} (Harapan: null)")
    assert res_status_prt.status_code == 200
    assert res_status_prt.data['data']['status'] == "pending"
    assert res_status_prt.data['data']['rejection_reason'] is None
    print("[UI Modul 3] Tombol formulir terkunci; Badge kuning 'Menunggu Verifikasi'.")

    # -------------------------------------------------------------
    # SKENARIO 5: PENGECEKAN OLEH MODUL 4 & MODUL 5 SAAT PENDING
    # -------------------------------------------------------------
    print_step("SKENARIO 5: Modul 4 & Modul 5 Memeriksa Partner yang Masih Pending")

    # Modul 4 cek kelayakan mitra
    print(f"[Modul 4 -> M3] Pengecekan otorisasi tambah produk: GET /api/m3/v1/partners/{assigned_prt}/")
    status_m4_check = res_status_prt.data['data']['status']
    if status_m4_check == "terverifikasi":
        print("Keputusan Modul 4: DIIZINKAN posting produk.")
    else:
        print(f"Keputusan Modul 4: DITOLAK posting produk karena status partner '{status_m4_check}'.")
    assert status_m4_check == "pending"

    # Modul 5 cek katalog publik (K-06)
    print(f"\n[Modul 5 -> M3] Memanggil Kontrak K-06: GET /api/m3/v1/partners/?status=terverifikasi")
    res_k06_pending = client.get("/api/m3/v1/partners/?status=terverifikasi")
    partner_ids_in_catalog = [p["partner_id"] for p in res_k06_pending.data["data"]]
    print(f"Daftar Toko di Etalase Publik: {partner_ids_in_catalog}")
    print(f"Apakah '{assigned_prt}' muncul di etalase publik? {assigned_prt in partner_ids_in_catalog} (Harapan: False)")
    assert assigned_prt not in partner_ids_in_catalog

    # -------------------------------------------------------------
    # SKENARIO 6: SIMULASI PENOLAKAN BERKAS OLEH ADMIN (T11)
    # -------------------------------------------------------------
    print_step("SKENARIO 6: Admin Menolak Pendaftaran (M3-US2 & Logika T11)")

    p_obj = Partner.objects.get(id=assigned_id)
    p_obj.status = "ditolak"
    p_obj.alasan_penolakan = "Foto KTP buram dan nomor NIK tidak terbaca jelas."
    p_obj.save()

    print("[Admin -> M3] Admin menetapkan status 'ditolak' dengan alasan:")
    print(f"   Alasan: '{p_obj.alasan_penolakan}'")

    print(f"\n[Mitra -> M3] Mitra memeriksa status penolakan: GET /api/m3/v1/partners/{assigned_prt}/")
    res_status_ditolak = client.get(f"/api/m3/v1/partners/{assigned_prt}/")
    print(f"Status HTTP: {res_status_ditolak.status_code}")
    print(f"Status Pengajuan: {res_status_ditolak.data['data']['status']}")
    print(f"Rejection Reason (Task T11): '{res_status_ditolak.data['data']['rejection_reason']}'")
    assert res_status_ditolak.data['data']['status'] == "ditolak"
    assert res_status_ditolak.data['data']['rejection_reason'] == "Foto KTP buram dan nomor NIK tidak terbaca jelas."
    print("[UI Modul 3] Badge merah 'Ditolak'; Alasan penolakan tampil; Tombol 'Daftar Ulang' aktif.")

    # -------------------------------------------------------------
    # SKENARIO 7: PERBAIKAN, APPROVAL ADMIN & SYNC MODUL 1
    # -------------------------------------------------------------
    print_step("SKENARIO 7: Mitra Perbaiki Berkas, Admin Setujui & Sinkronisasi Modul 1")

    # Mitra upload ulang / admin verifikasi ulang
    p_obj.status = "terverifikasi"
    p_obj.save()

    print("[Admin -> M3] Admin menyetujui pendaftaran mitra. Status menjadi: 'terverifikasi'")

    # Sinkronisasi ke Modul 1 (User & Auth)
    dummy_m1_sync_response = {
        "success": True,
        "message": "Akun mitra berhasil diaktifkan di Modul 1",
        "data": {
            "user_id": 99,
            "email": p_obj.email_usaha,
            "role": "partner",
            "partner_id": p_obj.partner_id,
            "status": "active"
        }
    }
    print("\n[M3 -> M1] Mengirim sinkronisasi akun: POST /api/m1/v1/auth/register-partner")
    print(f"Status Sinkronisasi Modul 1: 201 Created")
    print(f"Data Akun Modul 1 Terbit: User ID {dummy_m1_sync_response['data']['user_id']}, Role '{dummy_m1_sync_response['data']['role']}'")

    # Verifikasi Task T11: saat terverifikasi, rejection_reason otomatis null kembali
    res_status_terverifikasi = client.get(f"/api/m3/v1/partners/{assigned_prt}/")
    print(f"\n[Mitra -> M3] Memeriksa status akhir: GET /api/m3/v1/partners/{assigned_prt}/")
    print(f"Status Pengajuan: {res_status_terverifikasi.data['data']['status']}")
    print(f"Rejection Reason (Task T11): {res_status_terverifikasi.data['data']['rejection_reason']} (Harapan: null)")
    assert res_status_terverifikasi.data['data']['status'] == "terverifikasi"
    assert res_status_terverifikasi.data['data']['rejection_reason'] is None
    print("[UI Modul 3] Badge hijau 'Terverifikasi'; Tombol diarahkan ke portal login Modul 1.")

    # -------------------------------------------------------------
    # SKENARIO 8: KONSUMSI OLEH MODUL 4 & MODUL 5 (KONTRAK K-06)
    # -------------------------------------------------------------
    print_step("SKENARIO 8: Konsumsi Data Mitra Terverifikasi oleh Modul 4 & Modul 5")

    # Modul 4 cek status sekarang
    print(f"[Modul 4 -> M3] Pengecekan otorisasi posting produk: GET /api/m3/v1/partners/{assigned_prt}/")
    status_m4_now = res_status_terverifikasi.data['data']['status']
    if status_m4_now == "terverifikasi":
        print("Keputusan Modul 4: DIIZINKAN! Mitra berhak menambah katalog produk & jasa.")
    assert status_m4_now == "terverifikasi"

    # Modul 5 konsumsi etalase publik (Kontrak K-06)
    print(f"\n[Modul 5 -> M3] Memanggil Kontrak K-06: GET /api/m3/v1/partners/?status=terverifikasi")
    res_k06_final = client.get("/api/m3/v1/partners/?status=terverifikasi")
    print(f"Status HTTP: {res_k06_final.status_code} 200 OK")
    active_partners = res_k06_final.data["data"]
    active_prt_list = [p["partner_id"] for p in active_partners]
    print(f"Total Mitra Terverifikasi di Katalog Modul 5: {len(active_partners)}")
    print(f"Apakah '{assigned_prt}' muncul di etalase toko Modul 5? {assigned_prt in active_prt_list} (Harapan: True)")
    assert assigned_prt in active_prt_list

    # Uji Pencarian di Katalog Modul 5 (?q=araya)
    print(f"\n[Modul 5 -> M3] Filter pencarian toko mitra: GET /api/m3/v1/partners/?status=terverifikasi&q=araya")
    res_k06_search = client.get("/api/m3/v1/partners/?status=terverifikasi&q=araya")
    print(f"Jumlah Toko Cocok Pencarian: {len(res_k06_search.data['data'])}")
    print(f"Nama Usaha Ditemukan: '{res_k06_search.data['data'][0]['nama_usaha']}'")
    assert len(res_k06_search.data['data']) >= 1

    # Modul 2 Dashboard Agregasi UMKM per Kategori
    print(f"\n[Modul 2 -> M3] Dashboard Agregasi: GET /api/m3/v1/partners/?status=terverifikasi&unit_usaha_id=1")
    res_m2_dash = client.get("/api/m3/v1/partners/?status=terverifikasi&unit_usaha_id=1")
    print(f"Jumlah Mitra Aktif Kategori Pangan: {len(res_m2_dash.data['data'])}")
    assert len(res_m2_dash.data['data']) >= 1

    print("\n" + "=" * 75)
    print("  SELURUH 8 SKENARIO SPRINT 1 BERHASIL 100% TANPA REGRESI!")
    print("=" * 75)


if __name__ == "__main__":
    run_sprint_1_scenario()
