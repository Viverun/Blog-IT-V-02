from django.contrib.sites.models import Site
from django.conf import settings

class DynamicSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Update the Site domain if in development mode
        if settings.DEBUG and hasattr(settings, 'DOMAIN_NAME'):
            site = Site.objects.get(id=settings.SITE_ID)
            site.domain = settings.DOMAIN_NAME
            site.name = 'Blog-It Dev'
            site.save()
        
        response = self.get_response(request)
        return response