#!/bin/bash
set -e

echo "[1/4] Memeriksa virtual environment..."
if [ ! -d "venv" ]; then
    echo "Membuat virtual environment..."
    python3 -m venv venv
fi

echo "[2/4] Menginstal dependensi..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "[3/4] Menjalankan migrasi database..."
./venv/bin/python manage.py migrate

echo "[4/4] Menjalankan automated test..."
./venv/bin/python manage.py test partners

echo "Setup selesai. Jalankan server dengan:"
echo "./venv/bin/python manage.py runserver"
