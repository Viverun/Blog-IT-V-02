from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default='', blank=True)  # Added bio field with default empty string
    join_date = models.DateTimeField(auto_now_add=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"
        
    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        super().save(*args, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        
        try:
            # Check if image file exists and is accessible
            if self.image and hasattr(self.image, 'path') and os.path.exists(self.image.path):
                img = Image.open(self.image.path)
                
                # Check for image format
                img_format = img.format
                print(f"Image format: {img_format}, Mode: {img.mode}, Size: {img.size}")
                
                # Convert image format if necessary
                if img_format not in ['JPEG', 'PNG', 'GIF', 'WEBP']:
                    print(f"Converting image from {img_format} to JPEG")
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                
                # Resize if image is too large
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                
                # Optimize image quality - balance size vs. quality
                img.save(self.image.path, quality=85, optimize=True)
                
                # Print file size after optimization
                file_size = os.path.getsize(self.image.path) / 1024  # KB
                print(f"Image saved. File size: {file_size:.2f} KB")
        except Exception as e:
            # Log the error but don't crash            
            print(f"Error processing profile image: {str(e)}")
            # If we're in development, we might want to re-raise this
            if os.environ.get('DJANGO_DEBUG', 'True') == 'True':
                print("Debug mode is on, but not re-raising the exception to avoid breaking user experience")
                # We're not re-raising as it would break the user experience




