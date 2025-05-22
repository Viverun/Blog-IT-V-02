from django.contrib.sites.models import Site
from django.conf import settings
from urllib.parse import urlparse

class DynamicSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Always update the Site domain using SITE_URL from settings
        if hasattr(settings, "SITE_URL"):
            # Extract domain from SITE_URL (removing protocol)
            url_parts = urlparse(settings.SITE_URL)
            domain = url_parts.netloc
            
            # Only update if there is a valid domain
            if domain:
                try:
                    site = Site.objects.get(id=settings.SITE_ID)
                    
                    # Only update if the domain has changed
                    if site.domain != domain:
                        site.domain = domain
                        site.name = "Blog-It" if not settings.DEBUG else "Blog-It Dev"
                        site.save()
                except Exception as e:
                    # Log the error but do not crash
                    print(f"ERROR updating Site domain: {e}")
        
        response = self.get_response(request)
        return response

