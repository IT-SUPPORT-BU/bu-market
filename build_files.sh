#!/bin/bash
set -e

echo "==> Creating isolated Python build environment..."
python3 -m venv .build_venv
source .build_venv/bin/activate

echo "==> Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Running collectstatic..."
python manage.py collectstatic --noinput --clear

echo "==> Preparing output directory for Vercel CDN..."
mkdir -p staticfiles_build/static
cp -r staticfiles/* staticfiles_build/static/

echo "==> Cleaning up build environment..."
deactivate
rm -rf .build_venv

echo "==> Build complete!"
