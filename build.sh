#!/usr/bin/env bash
# Build script for Render
set -o errexit  # Exit on error

echo "--- Debugging file structure (Top of build.sh) ---"
echo "Current working directory (pwd): $(pwd)"
echo "Contents of current working directory (ls -la .):"
ls -la .
echo "Contents of /opt/render/project/src/ (ls -la /opt/render/project/src/):"
ls -la /opt/render/project/src/ || echo "Warning: Failed to list /opt/render/project/src/"
echo "--- End debugging file structure (Top) ---"

# Initial setup
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "--- Debugging file structure (After pip install) ---"
echo "Current working directory (pwd): $(pwd)"
echo "Contents of current working directory (ls -la .):"
ls -la .
echo "Contents of /opt/render/project/src/ (ls -la /opt/render/project/src/):"
ls -la /opt/render/project/src/ || echo "Warning: Failed to list /opt/render/project/src/"
echo "--- End debugging file structure (After pip install) ---"

# Collect static files
echo "Attempting to collect static files..."
# Try to run manage.py assuming it's in the current directory
if [ -f "manage.py" ]; then
    python manage.py collectstatic --no-input
else
    echo "Error: manage.py not found in current directory: $(pwd)"
    exit 1
fi

# Apply database migrations
echo "Attempting to apply database migrations..."
if [ -f "manage.py" ]; then
    python manage.py migrate
else
    echo "Error: manage.py not found in current directory: $(pwd) before migrate"
    exit 1
fi

echo "Build script completed."
