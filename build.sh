#!/usr/bin/env bash
# Build script for Render
set -o errexit  # Exit on error

# Initial setup
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
