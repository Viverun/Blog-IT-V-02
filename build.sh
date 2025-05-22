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

# Collect static files
echo "Attempting to collect static files with: python $MANAGE_PATH collectstatic --no-input"
python $MANAGE_PATH collectstatic --no-input

# Apply database migrations
echo "Attempting to apply database migrations with: python $MANAGE_PATH migrate"
python $MANAGE_PATH migrate

echo "Build script completed."
