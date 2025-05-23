from django.core.management.base import BaseCommand
from django.conf import settings
import os
import re
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Command(BaseCommand):
    help = 'Ensures the default profile picture is available in Cloudinary storage'

    def handle(self, *args, **options):
        # Only proceed if we're using Cloudinary in production
        if settings.DEBUG:
            self.stdout.write(self.style.NOTICE('Not in production (DEBUG=True). No action needed.'))
            return
        if 'cloudinary' not in settings.INSTALLED_APPS:
            self.stdout.write(self.style.NOTICE('Cloudinary not configured in INSTALLED_APPS. No action needed.'))
            return

        self.stdout.write(self.style.NOTICE('Production environment detected, checking default profile image in Cloudinary...'))
        
        # Print Cloudinary configuration information for debugging
        self.stdout.write(self.style.NOTICE('Cloudinary Configuration:'))
        cloudinary_url = os.environ.get('CLOUDINARY_URL', '')
        self.stdout.write('  CLOUDINARY_URL exists: {}'.format('CLOUDINARY_URL' in os.environ))

        # Configure Cloudinary directly from CLOUDINARY_URL
        if cloudinary_url:
            try:
                pattern = r"cloudinary://([^:]+):([^@]+)@([^/]+)"
                match = re.match(pattern, cloudinary_url)
                if match:
                    api_key = match.group(1)
                    api_secret = match.group(2)
                    cloud_name = match.group(3)
                    
                    # Configure Cloudinary
                    cloudinary.config(
                        cloud_name=cloud_name,
                        api_key=api_key,
                        api_secret=api_secret,
                        secure=True
                    )
                    self.stdout.write(self.style.SUCCESS('Successfully configured Cloudinary with cloud_name: {}'.format(cloud_name)))
                else:
                    self.stdout.write(self.style.ERROR('CLOUDINARY_URL format is invalid! Expected: cloudinary://API_KEY:API_SECRET@CLOUD_NAME'))
                    return
            except Exception as e:
                self.stdout.write(self.style.ERROR('Error parsing CLOUDINARY_URL: {}'.format(str(e))))
                return
        else:
            self.stdout.write(self.style.ERROR('CLOUDINARY_URL environment variable not found.'))
            return

        # Check if default.jpg exists in local media
        default_image_path = os.path.join(settings.BASE_DIR, 'media', 'default.jpg')
        if not os.path.exists(default_image_path):
            self.stdout.write(self.style.ERROR('Default image not found at {}'.format(default_image_path)))
            return

        # Check if default.jpg exists in Cloudinary
        cloudinary_default_exists = False
        try:
            # Check if the file exists by trying to get its info
            # Using media/default as the ID (without extension since Cloudinary strips it)
            result = cloudinary.api.resource('media/default')
            cloudinary_default_exists = True
            self.stdout.write(self.style.SUCCESS('Default profile image already exists in Cloudinary'))
            self.stdout.write('  URL: {}'.format(result['url']))
        except cloudinary.api.NotFound:
            self.stdout.write(self.style.WARNING('Default profile image not found in Cloudinary, will upload it'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Error checking if default image exists in Cloudinary: {}'.format(e)))

        # If default image doesn't exist in Cloudinary, upload it
        if not cloudinary_default_exists:
            try:
                # Read default image file
                with open(default_image_path, 'rb') as f:
                    default_image_content = f.read()

                # Upload to Cloudinary with public_id 'media/default' (so it is in the media folder)
                result = cloudinary.uploader.upload(
                    default_image_content,
                    public_id='media/default',
                    overwrite=True
                )
                self.stdout.write(self.style.SUCCESS('Successfully uploaded default profile image to Cloudinary'))
                self.stdout.write('Image URL: {}'.format(result["url"]))
            except Exception as e:
                self.stdout.write(self.style.ERROR('Error uploading default image to Cloudinary: {}'.format(e)))