from django.apps import AppConfig
import os


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        
        # Only run once when the app is ready, not during Django's auto-reload cycles
        if not os.environ.get('DJANGO_RELOADING'):
            os.environ['DJANGO_RELOADING'] = 'true'
            # Ensure default profile image is available in production
            try:
                from users.models import Profile
                Profile.ensure_default_image()
            except Exception as e:
                print(f"Error ensuring default profile image: {e}")