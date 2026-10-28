#!/bin/bash
set -e

echo "Menjalankan automated test partners..."
./venv/bin/python manage.py test partners -v 2
