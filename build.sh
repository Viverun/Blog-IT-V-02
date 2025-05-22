#!/usr/bin/env bash
# Build script for Render
set -o errexit  # Exit on error

# Initial setup
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Debugging: List files to understand the environment
echo "--- Debugging file structure ---"
echo "Current working directory: $(pwd)"
echo "Contents of current working directory (pwd):"
ls -la
echo "Contents of /opt/render/project/src/ (expected repo root):"
ls -la /opt/render/project/src/
echo "--- End debugging file structure ---"

# Collect static files
echo "Attempting to collect static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Attempting to apply database migrations..."
python manage.py migrate

echo "Build script completed."
