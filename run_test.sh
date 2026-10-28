#!/bin/bash
# ==============================================================================
# Script Otomatis Menjalankan Test Suite (Khusus Tester & QA)
# ==============================================================================

set -e

echo "🧪 Menjalankan Automated Test Suite Modul 3 (Partners)..."
./venv/bin/python manage.py test partners -v 2
