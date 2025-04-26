from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
import json
import sys
import os

# Simple test view that doesn't rely on any imports
def test_view(request):
    return HttpResponse("MCP Server test view works!")

# Import our AI tools - with fallback options
try:
    # First try to import from django_ai_tools as a module
    from django_ai_tools import get_model_structure, get_url_patterns, generate_view_context
except ImportError:
    # If that fails, try to import directly from the project root file
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from django_ai_tools import get_model_structure, get_url_patterns, generate_view_context
    except ImportError:
        # Fallbacks if the imports aren't available
        def get_model_structure(app_name=None):
            return {"error": "AI tools not available"}
            
        def get_url_patterns(app_name=None):
            return {"error": "AI tools not available"}
            
        def generate_view_context(request, **kwargs):
            return {"error": "AI tools not available"}


@staff_member_required
def ai_tools_dashboard(request):
    """
    Admin dashboard that shows the AI tools and model information.
    This view demonstrates how to use the AI tools in a Django view.
    """
    # Get model information for all apps or a specific app
    app_name = request.GET.get('app', None)
    
    try:
        model_data = get_model_structure(app_name)
        url_patterns = get_url_patterns(app_name)
        
        # Create a rich context for the template
        context = {
            'model_data': model_data,
            'url_patterns': url_patterns,
            'app_name': app_name,
            'available_apps': list(set(app_label for app_label in model_data.keys())) if isinstance(model_data, dict) else [],
        }
        
        # Return JSON if requested
        if request.GET.get('format') == 'json':
            return JsonResponse({
                'model_data': model_data,
                'url_patterns': url_patterns,
            })
        
        return render(request, 'mcp_server/ai_tools_dashboard.html', context)
    except Exception as e:
        # Return a helpful error page instead of 500 error
        return render(request, 'mcp_server/error.html', {
            'error': str(e),
            'error_type': type(e).__name__,
        })


def ai_model_info_api(request):
    """
    JSON API endpoint that provides model information.
    This can be used by AI tools to get project structure information.
    """
    try:
        app_name = request.GET.get('app', None)
        include_urls = request.GET.get('include_urls', 'false').lower() == 'true'
        
        response_data = {
            'model_data': get_model_structure(app_name),
        }
        
        if include_urls:
            response_data['url_patterns'] = get_url_patterns(app_name)
        
        # Add request context if needed
        if request.GET.get('include_context', 'false').lower() == 'true':
            response_data['context'] = generate_view_context(request)
        
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e), 'error_type': type(e).__name__}, status=500)
