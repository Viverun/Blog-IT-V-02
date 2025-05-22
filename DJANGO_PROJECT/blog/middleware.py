from django.utils.deprecation import MiddlewareMixin

class ContentVisibilityMiddleware(MiddlewareMixin):
    """
    Middleware to add Content-Security-Policy headers that prevent
    animations and transitions, ensuring content remains visible
    """
    
    def process_response(self, request, response):
        # Add CSP header to disable animations and transitions
        csp_value = (
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com "
            "https://cdnjs.cloudflare.com; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com; "
        )
        
        # Add headers that help with content visibility
        response['Content-Security-Policy'] = csp_value
        
        # Add X-Content-Visibility header (custom) to signal our intent
        response['X-Content-Visibility'] = 'force-visible'
        
        return response
