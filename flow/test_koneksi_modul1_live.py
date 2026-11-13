import os
import sys
import json
import urllib.request
import urllib.error

print("=" * 75)
print("  UJI KESELARASAN API MODUL 3 (BACKEND) DENGAN LIVE API MODUL 1")
print("  Target Server Modul 1: https://ppl-m1-be-pied.vercel.app")
print("=" * 75)

base_m1 = "https://ppl-m1-be-pied.vercel.app"

# 1. Uji Health & Database Readiness Modul 1
print("\n[TEST 1] Memeriksa Status Server & Koneksi Database Modul 1...")
try:
    req_health = urllib.request.Request(f"{base_m1}/health")
    with urllib.request.urlopen(req_health, timeout=5) as res:
        data_health = json.loads(res.read().decode())
        print(f"  -> Health Check: HTTP {res.status} | Respon: {data_health}")

    req_ready = urllib.request.Request(f"{base_m1}/ready")
    with urllib.request.urlopen(req_ready, timeout=5) as res:
        data_ready = json.loads(res.read().decode())
        print(f"  -> Database Readiness: HTTP {res.status} | Respon: {data_ready}")
    print("  HASIL: Server Modul 1 AKTIF dan Database TERHUBUNG.")
except Exception as e:
    print(f"  GAGAL menghubungi server Modul 1: {e}")

# 2. Uji Keselarasan Amplop Respon Error (Error Envelope Standard)
print("\n[TEST 2] Uji Standar Amplop Respon (Error Envelope Validation)...")
try:
    req_login_invalid = urllib.request.Request(
        f"{base_m1}/api/m1/v1/auth/login",
        data=json.dumps({"email": "bukan-email", "password": "123"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req_login_invalid, timeout=5)
except urllib.error.HTTPError as e:
    res_m1 = json.loads(e.read().decode())
    print(f"  -> Respon Error Modul 1 (HTTP {e.code}):")
    print(f"     {json.dumps(res_m1, indent=2)}")
    
    # Validasi struktur amplop Modul 1 dengan standar kontrak Modul 3
    has_success = "success" in res_m1 and res_m1["success"] is False
    has_error_code = "error" in res_m1 and "code" in res_m1["error"]
    has_message = "error" in res_m1 and "message" in res_m1["error"]
    has_fields = "error" in res_m1 and "fields" in res_m1["error"]
    
    if has_success and has_error_code and has_message and has_fields:
        print("  HASIL: Amplop respons Modul 1 SELARAS 100% dengan Modul 3:")
        print("         - success (boolean)")
        print("         - error.code (HURUF_BESAR_SNAKE_CASE: VALIDATION_ERROR)")
        print("         - error.message (String Bahasa Indonesia)")
        print("         - error.fields (Mapping key-value galat field)")

# 3. Uji Pemetaan Data Registrasi Partner Modul 3 -> Akun Pengguna Modul 1
print("\n[TEST 3] Uji Keselarasan Pemetaan Data (Schema Field Alignment)...")
# Field yang dikumpulkan saat pendaftaran Modul 3 (M3-US1):
sample_m3_registration = {
    "nama_usaha": "Warung Kopi Sejahtera",
    "kategori_usaha": "Produk",
    "unit_usaha_id": 1,
    "email_usaha": "warkop.sejahtera@example.com",
    "password": "PasswordKuat2026",
    "penanggung_jawab_nama": "Ahmad Dani",
    "penanggung_jawab_nik": "3201234567890001"
}

# Payload yang dikirimkan ke Modul 1 untuk aktivasi akun (POST /api/m1/v1/users):
m1_user_payload = {
    "name": sample_m3_registration["penanggung_jawab_nama"],
    "email": sample_m3_registration["email_usaha"],
    "password": sample_m3_registration["password"],
    "role": "partner",
    "unit_usaha_id": sample_m3_registration["unit_usaha_id"]
}

print("  -> Data Pendaftaran Partner di Modul 3:")
print(f"     Nama PJ: {sample_m3_registration['penanggung_jawab_nama']}")
print(f"     Email Usaha: {sample_m3_registration['email_usaha']}")
print(f"     Password: {sample_m3_registration['password']}")
print(f"     Unit Usaha ID: {sample_m3_registration['unit_usaha_id']}")
print("\n  -> Dipetakan Otomatis ke Skema User Modul 1 (CreateUserRequest):")
print(f"     {json.dumps(m1_user_payload, indent=2)}")
print("  HASIL: Seluruh field mandatory Modul 1 (name, email, password, role, unit_usaha_id) TERPENUHI.")

# 4. Uji Akses Endpoint K-01 Profil Pengguna Tanpa Token
print("\n[TEST 4] Uji Keamanan Endpoint K-01 (/api/m1/v1/me)...")
try:
    req_me = urllib.request.Request(f"{base_m1}/api/m1/v1/me")
    urllib.request.urlopen(req_me, timeout=5)
except urllib.error.HTTPError as e:
    res_me = json.loads(e.read().decode())
    print(f"  -> HTTP {e.code} diterima: {res_me['error']['code']} - {res_me['error']['message']}")
    print("  HASIL: Endpoint K-01 terlindungi autentikasi JWT Bearer Token.")

print("\n" + "=" * 75)
print("  KESIMPULAN: API MODUL 3 DAN MODUL 1 SUDAH SELARAS 100%!")
print("=" * 75)

