from django.urls import path
from . import views

# Simplified URL patterns without app_name namespace
urlpatterns = [
    path('ai-tools/', views.ai_tools_dashboard, name='mcp_ai_tools_dashboard'),
    path('api/model-info/', views.ai_model_info_api, name='mcp_ai_model_info_api'),
]