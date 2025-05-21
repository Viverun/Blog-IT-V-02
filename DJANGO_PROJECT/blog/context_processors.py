from .models import Tag
from django.db.models import Count
from .forms import SearchForm # Import SearchForm

def popular_tags(request):
    """Context processor that adds popular_tags to all templates"""
    tags = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
    return {'popular_tags': tags}

def search_form_context(request):
    """Context processor that adds search_form to all templates"""
    return {'search_form': SearchForm()}