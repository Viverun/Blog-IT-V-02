import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_PROJECT.settings')
django.setup()

# After Django is loaded, import the needed modules
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tempfile
import datetime

def test_cloudinary_connection():
    """Test connection to Cloudinary and media storage configuration."""
    print("\n===== CLOUDINARY CONNECTION TEST =====")
    
    # Check if Cloudinary is configured
    if 'cloudinary' in settings.INSTALLED_APPS:
        print("✅ Cloudinary app is installed")
    else:
        print("❌ Cloudinary app is NOT installed")
      # Check if Cloudinary storage is configured (Django 4.0+ format)
    storages_config = getattr(settings, 'STORAGES', {})
    default_storage_config = storages_config.get('default', {})
    storage_backend = default_storage_config.get('BACKEND', 'Not configured')
    
    if 'cloudinary' in storage_backend.lower():
        print("✅ Cloudinary is configured as the default storage backend")
    else:
        print(f"❌ Cloudinary is NOT configured as the default storage backend. Current: {storage_backend}")
        
        # Also check legacy setting for backwards compatibility
        legacy_storage = getattr(settings, 'DEFAULT_FILE_STORAGE', None)
        if legacy_storage and 'cloudinary' in legacy_storage.lower():
            print(f"   (Found in legacy DEFAULT_FILE_STORAGE: {legacy_storage})")
        elif legacy_storage:
            print(f"   (Legacy DEFAULT_FILE_STORAGE: {legacy_storage})")
    
    # Check environment variables
    if 'CLOUDINARY_URL' in os.environ:
        print("✅ CLOUDINARY_URL is set in environment")
        # Mask sensitive info when printing
        cloud_url = os.environ.get('CLOUDINARY_URL')
        if cloud_url:
            masked_url = cloud_url.split('@')[0][:15] + '...' + cloud_url.split('@')[-1][-10:]
            print(f"CLOUDINARY_URL format: {masked_url}")
    else:
        print("❌ CLOUDINARY_URL is NOT set in environment")
    
    # Try to upload a test file to test the connection
    print("\nAttempting to upload a test file...")
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.txt') as tmp:
            tmp.write(b'Test file content')
            tmp.flush()
            
            # Create a test path
            test_path = f'test_uploads/test-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.txt'
            
            # Try to save the file using the default storage
            with open(tmp.name, 'rb') as f:
                filename = default_storage.save(test_path, ContentFile(f.read()))
                
            # Check if file was uploaded
            if default_storage.exists(filename):
                file_url = default_storage.url(filename)
                print(f"✅ Test file uploaded successfully!")
                print(f"File URL: {file_url}")
                
                # Delete the test file
                default_storage.delete(filename)
                print("✅ Test file deleted successfully")
            else:
                print("❌ Test file was not uploaded correctly")
    except Exception as e:
        print(f"❌ Error during upload test: {str(e)}")
    
    print("\n===== END OF TEST =====\n")

def test_profile_image_update():
    """Try to update a profile image to test the functionality."""
    print("\n===== PROFILE IMAGE UPDATE TEST =====")
    
    try:
        from django.contrib.auth.models import User
        from users.models import Profile
        
        # Get the first user for testing
        users = User.objects.all()
        if not users.exists():
            print("❌ No users found in the database. Skipping profile image test.")
            return
        
        test_user = users.first()
        print(f"Using test user: {test_user.username}")
        
        # Get or create profile
        profile, created = Profile.objects.get_or_create(user=test_user)
        
        # Try to update profile image with a test image
        print("Attempting to update profile image...")
        
        # Create a temporary image file
        try:
            from PIL import Image as PILImage
            from io import BytesIO
            from django.core.files.uploadedfile import SimpleUploadedFile
            
            # Generate a simple test image
            img = PILImage.new('RGB', (200, 200), color='red')
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Create a SimpleUploadedFile
            test_image = SimpleUploadedFile(
                f"test-image-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.jpg",
                img_io.getvalue(),
                content_type='image/jpeg'
            )
            
            # Previous image path to compare later
            old_image_path = profile.image.name if profile.image else None
            
            # Update profile image
            profile.image = test_image
            profile.save()
            
            # Get the updated image URL
            profile.refresh_from_db()
            new_image_path = profile.image.name
            
            if new_image_path and new_image_path != old_image_path:
                print(f"✅ Profile image updated successfully!")
                print(f"Old image: {old_image_path}")
                print(f"New image: {new_image_path}")
                print(f"Image URL: {profile.image.url}")
            else:
                print("❌ Profile image was not updated correctly")
                print(f"Old image: {old_image_path}")
                print(f"New image: {new_image_path}")
        except Exception as e:
            print(f"❌ Error creating test image: {str(e)}")
    except Exception as e:
        print(f"❌ Error during profile image test: {str(e)}")
    
    print("\n===== END OF TEST =====\n")

if __name__ == '__main__':
    # Test both Cloudinary connection and profile image update
    test_cloudinary_connection()
    test_profile_image_update()
    
    print("\nIf Cloudinary is configured correctly but profile images still don't update,")
    print("please check the following:")
    print("1. Ensure CLOUDINARY_URL is properly set in your production environment")
    print("2. Check permissions on the Cloudinary account")
    print("3. Verify your form is properly configured with enctype='multipart/form-data'")
    print("4. Check for any JavaScript errors that might prevent form submission")
