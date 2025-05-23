from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Command(BaseCommand):
    help = 'Ensures the default profile picture is available in Cloudinary storage'

    def handle(self, *args, **options):
        # Only proceed if we're using Cloudinary
        if not settings.DEBUG and 'cloudinary' in settings.INSTALLED_APPS:
            self.stdout.write(self.style.NOTICE('Production environment detected, checking default profile image in Cloudinary...'))
            
            # Check if default.jpg exists in local media
            default_image_path = os.path.join(settings.BASE_DIR, 'media', 'default.jpg')
            
            if not os.path.exists(default_image_path):
                self.stdout.write(self.style.ERROR(f'Default image not found at {default_image_path}'))
                return
            
            # Check if default.jpg exists in Cloudinary
            cloudinary_default_exists = False
            try:
                # Check if the file exists by trying to get its info
                result = cloudinary.api.resource('default')
                cloudinary_default_exists = True
                self.stdout.write(self.style.SUCCESS('Default profile image already exists in Cloudinary'))
            except cloudinary.api.NotFound:
                self.stdout.write(self.style.WARNING('Default profile image not found in Cloudinary, will upload it'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error checking if default image exists in Cloudinary: {e}'))
            
            # If default image doesn't exist in Cloudinary, upload it
            if not cloudinary_default_exists:
                try:
                    # Read default image file
                    with open(default_image_path, 'rb') as f:
                        default_image_content = f.read()
                    
                    # Upload to Cloudinary with public_id 'default' (no extension)
                    # This will make it accessible as 'default.jpg' in Cloudinary
                    result = cloudinary.uploader.upload(
                        default_image_content,
                        public_id='default',
                        overwrite=True,
                        folder='media'  # Use the same folder structure as in settings.CLOUDINARY_STORAGE.PREFIX
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully uploaded default profile image to Cloudinary'))
                    self.stdout.write(f'Image URL: {result["url"]}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error uploading default image to Cloudinary: {e}'))
        else:
            self.stdout.write(self.style.NOTICE('Not in production or Cloudinary not configured. No action needed.'))
