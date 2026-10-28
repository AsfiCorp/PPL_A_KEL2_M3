#!/bin/bash
set -e

echo "Menjalankan automated test suite..."
./venv/bin/python manage.py test partners -v 2
