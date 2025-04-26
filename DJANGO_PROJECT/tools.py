"""
Django AI Assistant Tools

This module provides helper functions to interact with AI tools specifically
designed for Django applications. These tools help AI agents understand your
Django project structure, models, and URL patterns.
"""
import json
import requests
from django.conf import settings
from django.apps import apps
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField

# Default MCP server settings
MCP_SERVER_URL = getattr(settings, 'MCP_SERVER_URL', 'http://localhost:8080')


def get_model_structure(app_name=None):
    """
    Get the structure of Django models.
    
    Args:
        app_name (str, optional): Filter models by app name. If None, returns all models.
        
    Returns:
        dict: A dictionary containing model information.
    """
    try:
        # Try using MCP server if available
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/inspect_django_models",
            json={"app_name": app_name}
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        # Fallback to local implementation if server unavailable
        print(f"MCP server unavailable, using local implementation: {e}")
        return _get_model_structure_local(app_name)


def get_url_patterns(app_name=None):
    """
    Get the URL patterns defined in the project.
    
    Args:
        app_name (str, optional): Filter URLs by app name. If None, returns all URLs.
        
    Returns:
        dict: A dictionary containing URL pattern information.
    """
    try:
        # Try using MCP server if available
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/get_url_patterns",
            json={"app_name": app_name}
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        # Fallback to local implementation if server unavailable
        print(f"MCP server unavailable, using local implementation: {e}")
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


def _get_model_structure_local(app_name=None):
    """
    Local implementation of model structure inspection.
    
    Args:
        app_name (str, optional): Filter models by app name. If None, returns all models.
        
    Returns:
        dict: A dictionary containing model information.
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
