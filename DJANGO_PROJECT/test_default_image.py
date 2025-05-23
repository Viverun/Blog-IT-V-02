#!/usr/bin/env python
"""
Test script to verify the default profile image is properly configured in Cloudinary.
"""

import os
import sys
import django
import cloudinary
import cloudinary.api

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_PROJECT.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage

def test_default_image():
    """Test if the default profile image is available in Cloudinary."""
    print("\n===== DEFAULT PROFILE IMAGE TEST =====")
    
    # Check if we're in production mode with Cloudinary
    if settings.DEBUG:
        print("❌ Running in DEBUG mode. Cloudinary is not used in development.")
        return
    
    if 'cloudinary' not in settings.INSTALLED_APPS:
        print("❌ Cloudinary is not in INSTALLED_APPS. Cannot proceed with test.")
        return
    
    # Check storage configuration
    print(f"Using storage backend: {default_storage.__class__.__name__}")
    
    # Check if default.jpg exists in storage
    if default_storage.exists('default.jpg'):
        try:
            url = default_storage.url('default.jpg')
            print(f"✅ Default profile image exists in storage")
            print(f"URL: {url}")
        except Exception as e:
            print(f"❌ Error getting URL for default image: {str(e)}")
    else:
        print(f"❌ Default profile image does not exist in storage")
        
        # Try to check directly with Cloudinary API
        try:
            # Configure Cloudinary from settings
            if hasattr(settings, 'CLOUDINARY_STORAGE'):
                cloud_name = settings.CLOUDINARY_STORAGE.get('CLOUD_NAME')
                api_key = settings.CLOUDINARY_STORAGE.get('API_KEY')
                api_secret = settings.CLOUDINARY_STORAGE.get('API_SECRET')
                
                if cloud_name and api_key and api_secret:
                    cloudinary.config(
                        cloud_name=cloud_name,
                        api_key=api_key,
                        api_secret=api_secret
                    )
            
            # Try to get the image from Cloudinary
            result = cloudinary.api.resource('media/default')
            print(f"✅ Default image found in Cloudinary via direct API")
            print(f"URL: {result['url']}")
        except cloudinary.api.NotFound:
            print(f"❌ Default image not found in Cloudinary via direct API")
        except Exception as e:
            print(f"❌ Error checking Cloudinary directly: {str(e)}")
    
    print("\n===== CHECKING LOCAL DEFAULT IMAGE =====")
    # Check if local default image exists
    local_default_path = os.path.join(settings.BASE_DIR, 'media', 'default.jpg')
    if os.path.exists(local_default_path):
        print(f"✅ Local default image exists at: {local_default_path}")
        print(f"   This file can be uploaded to Cloudinary if needed.")
    else:
        print(f"❌ Local default image not found at: {local_default_path}")
        print(f"   You may need to create a default profile image and upload it to Cloudinary manually.")
    
    print("\n===== END OF TEST =====\n")

if __name__ == "__main__":
    test_default_image()
