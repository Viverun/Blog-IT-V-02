from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm # Removed commented-out import
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from django.core.exceptions import PermissionDenied # Removed unused import

def custom_logout(request):
    logout(request)
    # Force clear the session
    request.session.flush()
    # messages.success(request, 'You have been successfully logged out.') # Removed commented-out message
    return render(request, 'users/logout.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created! You are now able to Login!")
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
