# server.py
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_PROJECT.settings')
django.setup()

# Now we can import Django components
from django.apps import apps
from django.db.models import Model
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Blog MCP Server")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a custom tool for the blog application
@mcp.tool()
def greet(name: str) -> str:
    """Greet the user by name"""
    return f"Hello, {name}! Welcome to the Blog MCP Server."


# Add Django model inspector tool
@mcp.tool()
def inspect_django_models(app_name: str = None) -> dict:
    """
    Inspect Django models in the project.
    
    If app_name is provided, returns models only for that app.
    If app_name is None, returns all models from all installed apps.
    
    Returns a dictionary with model information including:
    - Field names and types
    - Relationships between models
    - Field constraints (nullable, unique, etc.)
    """
    result = {}
    
    # Get all models or filter by app_name
    if app_name:
        models = apps.get_app_config(app_name).get_models()
    else:
        models = apps.get_models()
    
    for model in models:
        model_name = model.__name__
        app_label = model._meta.app_label
        
        if app_label not in result:
            result[app_label] = {}
        
        # Get model fields
        fields = {}
        for field in model._meta.get_fields():
            field_info = {
                'type': field.__class__.__name__,
                'nullable': getattr(field, 'null', True),
                'blank': getattr(field, 'blank', True),
            }
            
            # Handle relationship fields
            if isinstance(field, ForeignKey):
                field_info['relates_to'] = {
                    'model': field.related_model.__name__,
                    'app': field.related_model._meta.app_label,
                }
            elif isinstance(field, ManyToManyField):
                field_info['relates_to'] = {
                    'model': field.related_model.__name__,
                    'app': field.related_model._meta.app_label,
                    'type': 'many-to-many',
                }
            elif isinstance(field, OneToOneField):
                field_info['relates_to'] = {
                    'model': field.related_model.__name__,
                    'app': field.related_model._meta.app_label,
                    'type': 'one-to-one',
                }
                
            fields[field.name] = field_info
            
        result[app_label][model_name] = {
            'fields': fields,
            'verbose_name': str(model._meta.verbose_name),
            'verbose_name_plural': str(model._meta.verbose_name_plural),
        }
    
    return result


# Add a tool to get URL patterns from a Django app
@mcp.tool()
def get_url_patterns(app_name: str = None) -> dict:
    """
    Get URL patterns from Django apps.
    
    If app_name is provided, returns URLs only for that app.
    If app_name is None, returns all URLs from all installed apps.
    """
    from django.urls import get_resolver
    
    result = {}
    resolver = get_resolver()
    
    def extract_patterns(patterns, parent_path=''):
        urls = []
        for pattern in patterns:
            path = parent_path + str(pattern.pattern)
            if hasattr(pattern, 'callback') and pattern.callback:
                # Get the view function details
                view_name = pattern.callback.__name__
                module_name = pattern.callback.__module__
                
                if app_name and not module_name.startswith(app_name):
                    continue
                    
                urls.append({
                    'path': path,
                    'view': view_name,
                    'module': module_name,
                    'name': pattern.name,
                })
            
            # Recursive handling of included patterns
            if hasattr(pattern, 'url_patterns'):
                urls.extend(extract_patterns(pattern.url_patterns, path))
                
        return urls
    
    result['url_patterns'] = extract_patterns(resolver.url_patterns)
    return result


# Start the server if this script is run directly
if __name__ == "__main__":
    print("Starting MCP Server...")
    # Fix: use the correct syntax for running the FastMCP server
    try:
        # Try without arguments first
        mcp.run()
    except TypeError:
        # If that doesn't work, try with positional arguments
        try:
            mcp.run("0.0.0.0", 8080)
        except:
            # If all else fails, try using uvicorn directly
            import uvicorn
            uvicorn.run("server:mcp", host="0.0.0.0", port=8080)