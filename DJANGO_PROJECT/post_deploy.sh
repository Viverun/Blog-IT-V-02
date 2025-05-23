#!/bin/bash
# Script to run after deployment to ensure default profile image is uploaded to Cloudinary

echo "Running post-deployment tasks..."

# Run Django management command to ensure default profile image is uploaded to Cloudinary
python manage.py ensure_default_profile_image

echo "Post-deployment tasks completed."
