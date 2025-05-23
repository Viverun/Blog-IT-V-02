from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
from django.conf import settings as django_settings
from django.core.files.storage import default_storage as current_default_storage
import importlib.util
import re

# Check if Cloudinary is available
CLOUDINARY_AVAILABLE = False
MediaCloudinaryStorage = None

if importlib.util.find_spec("cloudinary_storage"):
    try:
        from cloudinary_storage.storage import MediaCloudinaryStorage
        CLOUDINARY_AVAILABLE = True
    except ImportError:
        pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default='', blank=True)
    join_date = models.DateTimeField(auto_now_add=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    @classmethod
    def ensure_default_image(cls):
        """Ensures the default profile image exists in the current storage backend."""
        if not django_settings.DEBUG and CLOUDINARY_AVAILABLE:
            if not current_default_storage.exists('default.jpg'):
                print("[PROFILE_MODEL] Default image doesn't exist in storage, trying to upload it")
                
                default_image_path = os.path.join(django_settings.BASE_DIR, 'media', 'default.jpg')
                
                if not os.path.exists(default_image_path):
                    print("[PROFILE_MODEL] Default image not found at {}".format(default_image_path))
                    return
                
                try:
                    cloudinary_spec = importlib.util.find_spec("cloudinary")
                    if cloudinary_spec:
                        import cloudinary
                        import cloudinary.uploader
                        
                        cloudinary_url = os.environ.get('CLOUDINARY_URL', '')
                        if not cloudinary_url:
                            print("[PROFILE_MODEL] No CLOUDINARY_URL found in environment")
                            return
                        
                        pattern = r"cloudinary://([^:]+):([^@]+)@([^/]+)"
                        match = re.match(pattern, cloudinary_url)
                        if not match:
                            print("[PROFILE_MODEL] Invalid CLOUDINARY_URL format")
                            return
                        
                        try:
                            api_key, api_secret, cloud_name = match.groups()
                            
                            cloudinary.config(
                                cloud_name=cloud_name,
                                api_key=api_key,
                                api_secret=api_secret,
                                secure=True
                            )
                            print("[PROFILE_MODEL] Successfully configured Cloudinary with cloud_name: {}".format(cloud_name))
                            
                            with open(default_image_path, 'rb') as f:
                                upload_result = cloudinary.uploader.upload(
                                    f.read(),
                                    public_id='media/default',
                                    overwrite=True
                                )
                                if upload_result and 'url' in upload_result:
                                    print("[PROFILE_MODEL] Default image uploaded directly to Cloudinary: {}".format(upload_result['url']))
                                    return
                                
                        except Exception as cloud_error:
                            print("[PROFILE_MODEL] Cloudinary upload error: {}".format(cloud_error))
                    
                    # Fall back to normal storage API if direct upload fails
                    with open(default_image_path, 'rb') as f:
                        from django.core.files.base import ContentFile
                        current_default_storage.save('default.jpg', ContentFile(f.read()))
                    print("[PROFILE_MODEL] Default image uploaded using storage API")
                    
                except Exception as e:
                    print("[PROFILE_MODEL] Error uploading default image: {}".format(e))
            else:
                print("[PROFILE_MODEL] Default image already exists in storage")

    def save(self, *args, **kwargs):
        print("[PROFILE_SAVE_ENTRY] User: {}, Current Image: {}".format(self.user.username, self.image))
        print("[PROFILE_SAVE_ENTRY] DEBUG from settings: {}".format(django_settings.DEBUG))
        print("[PROFILE_SAVE_ENTRY] django_settings.STORAGES['default']: {}".format(django_settings.STORAGES['default']['BACKEND']))
        print("[PROFILE_SAVE_ENTRY] Current default_storage IS: {}".format(current_default_storage))
        print("[PROFILE_SAVE_ENTRY] self.image.storage IS: {}".format(self.image.storage))

        # Only process the image if it's not the default image and we're in DEBUG mode (local development)
        if self.image.name != 'default.jpg':
            print("[PROFILE_SAVE_PIL] Processing uploaded image: {}".format(self.image.name))
            try:
                # Save the model first so the image is saved to disk
                super().save(*args, **kwargs)
                # Then process with PIL
                if django_settings.DEBUG:  # Only resize locally
                    img_path = self.image.path  # Get the file path
                    try:
                        img = Image.open(img_path)
                        if img.height > 300 or img.width > 300:
                            output_size = (300, 300)
                            img.thumbnail(output_size)
                            img.save(img_path)
                            print("[PROFILE_SAVE_PIL] Image resized to 300x300")
                    except Exception as img_error:
                        print("[PROFILE_SAVE_PIL] Error processing image: {}".format(img_error))
            except Exception as e:
                print("[PROFILE_SAVE_PIL] Error saving/processing profile: {}".format(e))
                if not django_settings.DEBUG:
                    raise  # Re-raise in production to ensure we catch all errors
        else:
            print("[PROFILE_SAVE_PIL] Image is default.jpg, no PIL processing needed.")
            super().save(*args, **kwargs)