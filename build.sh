#!/usr/bin/env bash
# Build script for Render
set -o errexit  # Exit on error

echo "--- Debugging file structure (Top of build.sh) ---"
echo "Current working directory (pwd): $(pwd)"
echo "Contents of current working directory (ls -la .):"
ls -la .
echo "Checking if DJANGO_PROJECT directory exists and what's in it:"
if [ -d "DJANGO_PROJECT" ]; then
    echo "Contents of DJANGO_PROJECT directory:"
    ls -la DJANGO_PROJECT
else
    echo "DJANGO_PROJECT directory not found!"
fi
echo "--- End debugging file structure (Top) ---"

# Initial setup
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "--- Debugging file structure (After pip install) ---"
echo "Current working directory (pwd): $(pwd)"
echo "Contents of current working directory (ls -la .):"
ls -la .
echo "--- End debugging file structure (After pip install) ---"

# Check where manage.py might be
echo "Looking for manage.py in possible locations..."
if [ -f "manage.py" ]; then
    echo "Found manage.py in current directory"
    MANAGE_PATH="./manage.py"
elif [ -f "DJANGO_PROJECT/manage.py" ]; then
    echo "Found manage.py in DJANGO_PROJECT/ directory"
    MANAGE_PATH="DJANGO_PROJECT/manage.py"
else
    echo "Error: manage.py not found in expected locations!"
    find . -name "manage.py" -type f | sort
    exit 1
fi

# Python path and module import check
echo "--- Python Path and Module Import Check ---"
python -c "import sys; print('sys.path:', sys.path); import cloudinary_storage; print('cloudinary_storage imported successfully')" || echo "Failed to import cloudinary_storage directly"

# Check Cloudinary configuration
echo "--- Checking Cloudinary Configuration ---"
python -c "
import os
print('CLOUDINARY_URL environment variable exists:', 'CLOUDINARY_URL' in os.environ)
if 'CLOUDINARY_URL' in os.environ:
    url = os.environ.get('CLOUDINARY_URL')
    # Mask the URL for security
    if url and len(url) > 20:
        masked_url = url[:15] + '...' + url[-5:]
        print('CLOUDINARY_URL value (masked):', masked_url)
    else:
        print('CLOUDINARY_URL is set but appears to be invalid')
else:
    print('Individual Cloudinary variables:')
    print('  CLOUDINARY_CLOUD_NAME exists:', 'CLOUDINARY_CLOUD_NAME' in os.environ)
    print('  CLOUDINARY_API_KEY exists:', 'CLOUDINARY_API_KEY' in os.environ)
    print('  CLOUDINARY_API_SECRET exists:', 'CLOUDINARY_API_SECRET' in os.environ)
print('---')
" || echo "Failed to check Cloudinary configuration"
echo "--- End Cloudinary Configuration Check ---"

# Explicitly set the Django settings module
export DJANGO_SETTINGS_MODULE=DJANGO_PROJECT.settings

# List Django management commands for debugging
echo "--- Listing Django Management Commands ---"
python $MANAGE_PATH
echo "--- End Listing Django Management Commands ---"

# Collect static files
echo "Attempting to collect static files with: python $MANAGE_PATH collectstatic --no-input"
python $MANAGE_PATH collectstatic --no-input

# Apply database migrations
echo "Attempting to apply database migrations with: python $MANAGE_PATH migrate"
python $MANAGE_PATH migrate

# Update the default Site domain to match our settings
echo "Updating the default Site domain from settings.SITE_URL"
python $MANAGE_PATH shell -c "
from django.contrib.sites.models import Site
from django.conf import settings
from urllib.parse import urlparse
if hasattr(settings, 'SITE_URL'):
    url_parts = urlparse(settings.SITE_URL)
    domain = url_parts.netloc
    if domain:
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = domain
        site.name = 'Blog-It'
        site.save()
        print(f'SUCCESS: Site domain updated to {domain}')
    else:
        print('ERROR: No valid domain in settings.SITE_URL')
else:
    print('ERROR: settings.SITE_URL not found')
"

echo "Build script completed."
