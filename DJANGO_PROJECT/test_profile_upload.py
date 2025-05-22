#!/usr/bin/env python
"""
Test script to simulate uploading a profile picture in your Django application.
This script tests the integration between Django and Cloudinary by simulating
a file upload similar to what happens when a user updates their profile picture.

Requires a running Django application with proper Cloudinary configuration.
"""

import os
import sys
import django

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_PROJECT.settings')
django.setup()

# Import Django-specific modules after setup
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import Profile
from django.conf import settings

def test_profile_image_upload():
    """
    Test the profile image upload functionality using a test image.
    """
    print(f"Django DEBUG mode is: {settings.DEBUG}")
    print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    # Check if Cloudinary is properly configured
    cloudinary_configured = False
    if hasattr(settings, 'CLOUDINARY_STORAGE') and settings.CLOUDINARY_STORAGE:
        cloud_name = settings.CLOUDINARY_STORAGE.get('CLOUD_NAME')
        api_key = settings.CLOUDINARY_STORAGE.get('API_KEY')
        if cloud_name and api_key:
            cloudinary_configured = True
            print(f"Cloudinary is configured with cloud_name: {cloud_name}")
            
            # Mask the API key for security
            masked_key = api_key[:4] + "*" * (len(api_key) - 4) if api_key and len(api_key) > 4 else "****"
            print(f"API Key: {masked_key}")
    
    if not cloudinary_configured and not settings.DEBUG:
        print("WARNING: Cloudinary does not appear to be properly configured in production mode.")
        print("Check your CLOUDINARY_URL or individual Cloudinary credential environment variables.")
    
    # Get or create a test user
    username = "testuser_image_upload"
    try:
        user = User.objects.get(username=username)
        print(f"Using existing test user: {username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email="testuser@example.com",
            password="complexpassword123"
        )
        print(f"Created new test user: {username}")
    
    # Get the user's profile
    profile = Profile.objects.get(user=user)
    
    # Test image path - using a sample image in the media directory
    test_image_path = os.path.join(settings.BASE_DIR, 'media', 'default.jpg')
    
    if not os.path.exists(test_image_path):
        print(f"Error: Test image not found at {test_image_path}")
        return
    
    # Read the test image
    with open(test_image_path, 'rb') as f:
        image_content = f.read()
    
    # Create a SimpleUploadedFile
    image_file = SimpleUploadedFile(
        name='test_profile_image.jpg',
        content=image_content,
        content_type='image/jpeg'
    )
    
    # Store the previous image name for comparison
    previous_image = profile.image.name if profile.image else None
    print(f"Previous profile image: {previous_image}")
    
    # Update the profile with the new image
    profile.image = image_file
    profile.save()
    
    # Refresh the profile from the database
    profile.refresh_from_db()
    
    # Print the new image name
    print(f"New profile image: {profile.image.name}")
    
    # Check if the image changed
    if profile.image.name != previous_image:
        print("SUCCESS: Profile image was successfully updated!")
        
        # Try to get the URL
        try:
            image_url = profile.image.url
            print(f"Image URL: {image_url}")
        except Exception as e:
            print(f"WARNING: Could not get image URL: {e}")
    else:
        print("ERROR: Profile image was not updated.")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_profile_image_upload()
