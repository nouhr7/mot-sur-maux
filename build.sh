#!/usr/bin/env bash
# Build step for Render (and similar hosts): install, collect static, migrate.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
