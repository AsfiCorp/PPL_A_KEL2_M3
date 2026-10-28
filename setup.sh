#!/bin/bash
# ==============================================================================
# Script Otomatis Setup Backend - Araya Business Hub (Modul 3)
# Khusus Frontend, Backend, dan Tester
# ==============================================================================

set -e

echo "🚀 [1/4] Memeriksa Virtual Environment..."
if [ ! -d "venv" ]; then
    echo "📦 Membuat virtual environment (venv)..."
    python3 -m venv venv
else
    echo "✓ Virtual environment sudah ada."
fi

echo "📦 [2/4] Menginstal dependensi..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "🗄️  [3/4] Menjalankan migrasi database SQLite..."
./venv/bin/python manage.py migrate

echo "✅ [4/4] Menjalankan automated test untuk verifikasi..."
./venv/bin/python manage.py test partners

echo ""
echo "🎉 Setup selesai! Untuk menjalankan development server, jalankan:"
echo "   ./venv/bin/python manage.py runserver"
echo "   API akan berjalan di: http://127.0.0.1:8000/"
