from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

# Import our AI tools
from django_ai_tools import get_model_structure, generate_view_context

def custom_logout(request):
    logout(request)
    # Force clear the session
    request.session.flush()
    # messages.success(request, 'You have been successfully logged out.')
    return render(request, 'users/logout.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your Account has been created! You are now able to Login!")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request,'users/register.html',{'form': form})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    # Removed the automatic redirect to allow users to see their own public profile
    
    # Get the user's posts
    from blog.models import Post
    user_posts = Post.objects.filter(author=user).order_by('-date_posted')

    context = {
        'profile_user': user,
        'user_posts': user_posts,
    }
    return render(request, 'users/user_profile.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')  # Optional: redirect after POST
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def profile_ai_assist(request):
    """
    Endpoint that provides AI-assisted suggestions for user profiles.
    This view demonstrates how AI tools can be integrated into your app.
    """
    # Check if it's an AI assistance request
    if request.GET.get('ai_assist') == 'true':
        # Generate rich context for AI tools
        context_data = generate_view_context(request, 
            user_info={
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'date_joined': request.user.date_joined.isoformat(),
                'last_login': request.user.last_login.isoformat() if request.user.last_login else None,
                'is_staff': request.user.is_staff,
                'is_active': request.user.is_active,
            }
        )
        
        # Get model structure for the User and Profile models
        model_data = get_model_structure('users')
        
        # Return JSON response with combined data
        return JsonResponse({
            'context': context_data,
            'model_data': model_data,
            'message': "This endpoint provides data for AI tools to assist with user profiles."
        })
    
    # Regular request - redirect to profile page
    return redirect('profile')
