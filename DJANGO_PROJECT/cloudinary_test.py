#!/usr/bin/env python
"""
Test script to verify Cloudinary configuration without running the full Django app.
This script can be run directly to check if your Cloudinary credentials are correct.
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# Try to import cloudinary
try:
    import cloudinary
    import cloudinary.uploader
    print("✓ Cloudinary module imported successfully")
except ImportError:
    print("✗ Failed to import cloudinary. Run: pip install cloudinary")
    sys.exit(1)

# Try to import django-cloudinary-storage
try:
    import cloudinary_storage
    print("✓ Cloudinary Storage module imported successfully")
except ImportError:
    print("✗ Failed to import cloudinary_storage. Run: pip install django-cloudinary-storage")
    sys.exit(1)

# Load environment variables from .env file if it exists
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print("✓ Loaded environment variables from {}".format(env_path))
else:
    print("! No .env file found at {}. Using system environment variables.".format(env_path))

# Check for Cloudinary credentials
cloudinary_url = os.environ.get('CLOUDINARY_URL')
cloudinary_cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
cloudinary_api_key = os.environ.get('CLOUDINARY_API_KEY')
cloudinary_api_secret = os.environ.get('CLOUDINARY_API_SECRET')

if cloudinary_url:
    print("✓ CLOUDINARY_URL environment variable found")
    # Parse CLOUDINARY_URL
    try:
        pattern = r"cloudinary://([^:]+):([^@]+)@([^/]+)"
        match = re.match(pattern, cloudinary_url)
        if match:
            api_key = match.group(1)
            api_secret = match.group(2)
            cloud_name = match.group(3)
            
            masked_key = api_key[:4] + "*" * (len(api_key) - 4) if api_key and len(api_key) > 4 else "****"
            masked_secret = api_secret[:4] + "*" * (len(api_secret) - 4) if api_secret and len(api_secret) > 4 else "****"
            
            print("✓ Parsed CLOUDINARY_URL successfully:")
            print("  - Cloud Name: {}".format(cloud_name))
            print("  - API Key: {}".format(masked_key))
            print("  - API Secret: {}".format(masked_secret))
            
            # Configure Cloudinary
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True
            )
            print("✓ Configured cloudinary with parsed values")
        else:
            print("✗ CLOUDINARY_URL format is invalid! Expected: cloudinary://API_KEY:API_SECRET@CLOUD_NAME")
            sys.exit(1)
    except Exception as e:
        print("✗ Error parsing CLOUDINARY_URL: {}".format(str(e)))
        sys.exit(1)
elif cloudinary_cloud_name and cloudinary_api_key and cloudinary_api_secret:
    print("✓ Individual Cloudinary credential environment variables found")
    
    masked_key = cloudinary_api_key[:4] + "*" * (len(cloudinary_api_key) - 4) if cloudinary_api_key and len(cloudinary_api_key) > 4 else "****"
    masked_secret = cloudinary_api_secret[:4] + "*" * (len(cloudinary_api_secret) - 4) if cloudinary_api_secret and len(cloudinary_api_secret) > 4 else "****"
    
    print("  - Cloud Name: {}".format(cloudinary_cloud_name))
    print("  - API Key: {}".format(masked_key))
    print("  - API Secret: {}".format(masked_secret))
    
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=cloudinary_cloud_name,
        api_key=cloudinary_api_key,
        api_secret=cloudinary_api_secret,
        secure=True
    )
    print("✓ Configured cloudinary with individual credential values")
else:
    print("✗ No Cloudinary credentials found in environment variables!")
    print("  Please set either CLOUDINARY_URL or all of these:")
    print("  - CLOUDINARY_CLOUD_NAME")
    print("  - CLOUDINARY_API_KEY")
    print("  - CLOUDINARY_API_SECRET")
    sys.exit(1)

# Test Cloudinary connection
print("\nTesting Cloudinary connection...")
try:
    # Generate a unique timestamp for the test image
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # A simple test upload using a placeholder image
    print("Attempting to upload a test image...")
    test_upload = cloudinary.uploader.upload(
        "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg",
        public_id="test-image-{}".format(timestamp)
    )
    
    if test_upload and 'public_id' in test_upload:
        print("✓ Successfully uploaded test image to Cloudinary!")
        print("  Public ID: {}".format(test_upload['public_id']))
        print("  URL: {}".format(test_upload['url']))
    else:
        print("✗ Upload test returned unexpected result")
        sys.exit(1)
except Exception as e:
    print("✗ Failed to connect to Cloudinary: {}".format(str(e)))
    print("  Please check your Cloudinary credentials and internet connection.")
    sys.exit(1)

print("\n--- Cloudinary Configuration Test Successful ---")
