from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os # Ensure os is imported
from django.conf import settings as django_settings # Add this import
from django.core.files.storage import default_storage as current_default_storage # Add this import
import importlib.util # For checking module availability

# Check if Cloudinary is installed and configured
CLOUDINARY_AVAILABLE = False
MediaCloudinaryStorage = None
if importlib.util.find_spec("cloudinary") and importlib.util.find_spec("cloudinary_storage"):
    try:
        from cloudinary_storage.storage import MediaCloudinaryStorage
        CLOUDINARY_AVAILABLE = True
    except ImportError:
        CLOUDINARY_AVAILABLE = False 
        MediaCloudinaryStorage = None

CLOUDINARY_DIRECT_AVAILABLE = False
if importlib.util.find_spec("cloudinary"):
    CLOUDINARY_DIRECT_AVAILABLE = True

# Try to import cloudinary for direct API access in the ensure_default_image method
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The ImageField works with both local storage and Cloudinary through DEFAULT_FILE_STORAGE
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default='', blank=True)
    join_date = models.DateTimeField(auto_now_add=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)

    @classmethod
    def ensure_default_image(cls):
        """Ensures the default profile image exists in the current storage backend."""
        # Use CLOUDINARY_AVAILABLE for checking if cloudinary_storage is in use
        if not django_settings.DEBUG and CLOUDINARY_AVAILABLE:
            # Check if default.jpg exists in storage
            if not current_default_storage.exists('default.jpg'):
                print("[PROFILE_MODEL] Default image doesn't exist in storage, trying to upload it")
                
                # Try to upload the default image from local media
                default_image_path = os.path.join(django_settings.BASE_DIR, 'media', 'default.jpg')
                
                if os.path.exists(default_image_path):
                    try:
                        with open(default_image_path, 'rb') as f:
                            from django.core.files.base import ContentFile # Ensure ContentFile is used
                            current_default_storage.save('default.jpg', ContentFile(f.read()))
                        print("[PROFILE_MODEL] Default image uploaded to storage successfully")
                    except Exception as e:
                        print(f"[PROFILE_MODEL] Error uploading default image to storage: {e}")
                else:
                    print(f"[PROFILE_MODEL] Default image not found at {default_image_path}")
            else:
                print("[PROFILE_MODEL] Default image already exists in storage")

    def __str__(self):
        return f"{self.user.username} Profile"
        
    def save(self, *args, **kwargs):
        print(f"[PROFILE_SAVE_ENTRY] User: {self.user.username}, Current Image: {self.image.name if self.image else 'No Image'}")
        print(f"[PROFILE_SAVE_ENTRY] DEBUG from settings: {django_settings.DEBUG}")
        print(f"[PROFILE_SAVE_ENTRY] django_settings.STORAGES['default']: {django_settings.STORAGES.get('default', {}).get('BACKEND', 'Not Set')}")
        print(f"[PROFILE_SAVE_ENTRY] Current default_storage IS: {current_default_storage}")
        if self.image and hasattr(self.image, 'storage'):
            print(f"[PROFILE_SAVE_ENTRY] self.image.storage IS: {self.image.storage}")

        super().save(*args, **kwargs) # Call the "real" save() method.
        
        try:
            if self.image and self.image.name and self.image.name != 'default.jpg':
                image_instance = self.image # Use the instance's image attribute
                storage_being_used = image_instance.storage
                print(f"[PROFILE_SAVE_POST_SUPER] Processing image: {image_instance.name}, Storage: {storage_being_used}")

                try:
                    url = image_instance.url
                    print(f"[PROFILE_SAVE_POST_SUPER] Image URL via storage: {url}")
                except Exception as e_url:
                    print(f"[PROFILE_SAVE_POST_SUPER] Error getting image URL: {e_url}")

                is_cloudinary = CLOUDINARY_AVAILABLE and MediaCloudinaryStorage and isinstance(storage_being_used, MediaCloudinaryStorage)
                
                if not is_cloudinary and hasattr(image_instance, 'path') and image_instance.path and os.path.exists(image_instance.path):
                    print(f"[PROFILE_SAVE_PIL] Processing image locally: {image_instance.path}")
                    img = Image.open(image_instance.path)
                    
                    original_format = img.format
                    original_mode = img.mode
                    original_size = img.size
                    print(f"Original image - Format: {original_format}, Mode: {original_mode}, Size: {original_size}")
                    
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        print(f"Image resized to fit within 300x300. New size: {img.size}")
                    
                    save_kwargs = {'quality': 85, 'optimize': True}
                    if original_format:
                        save_kwargs['format'] = original_format
                    
                    img.save(image_instance.path, **save_kwargs)
                    
                    file_size_kb = os.path.getsize(image_instance.path) / 1024
                    print(f"Image saved after PIL. File size: {file_size_kb:.2f} KB. Path: {image_instance.path}")
                elif is_cloudinary:
                    print(f"[PROFILE_SAVE_PIL] Image is on Cloudinary. Name: {image_instance.name}. No local PIL processing applied here.")
                else:
                    print(f"[PROFILE_SAVE_PIL] Image storage is not local FS or not Cloudinary, or path not available. Name: {image_instance.name}, Storage: {storage_being_used}")

            elif self.image and self.image.name == 'default.jpg':
                print("[PROFILE_SAVE_PIL] Image is default.jpg, no PIL processing needed.")
            else:
                print("[PROFILE_SAVE_PIL] No image attached or image name is empty, no PIL processing.")
        except FileNotFoundError as fnf_error:
            print(f"Error during PIL image processing (FileNotFound): {str(fnf_error)}. Image path: {image_instance.path if 'image_instance' in locals() and hasattr(image_instance, 'path') else 'N/A'}")
        except Exception as e:
            print(f"Error during PIL image processing in Profile.save: {str(e)}")
            if django_settings.DEBUG:
                 print("Debug mode is on, but not re-raising the exception to avoid breaking user experience")
