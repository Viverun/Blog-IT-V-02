from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width> 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)




