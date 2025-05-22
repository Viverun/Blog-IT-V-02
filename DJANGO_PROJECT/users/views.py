from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm # Removed commented-out import
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
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
            try:
                u_form.save()
                profile = p_form.save(commit=False)
                
                # Check if there's a file upload
                if 'image' in request.FILES:
                    image_file = request.FILES['image']
                    
                    # Additional file validation
                    # Max file size (2MB)
                    max_size = 2 * 1024 * 1024
                    if image_file.size > max_size:
                        raise ValueError(f"The uploaded image exceeds the maximum file size of 2MB. Current size: {image_file.size / 1024 / 1024:.2f}MB")
                    
                    # Check image file extension
                    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                    ext = os.path.splitext(image_file.name)[1].lower()
                    if ext not in valid_extensions:
                        raise ValueError(f"Invalid file type. Only {', '.join(valid_extensions)} are supported.")
                    
                    # Log information about the uploaded file
                    print(f"File upload validated: {image_file.name}, Size: {image_file.size} bytes, Type: {image_file.content_type}")                # Save the profile
                profile.save()
                
                messages.success(request, 'Your profile has been updated successfully!')
                from django.urls import reverse
                from django.http import HttpResponseRedirect
                return HttpResponseRedirect(reverse('profile') + '?status=success')
            except ValueError as ve:
                # Handle validation errors
                messages.error(request, str(ve))
            except Exception as e:
                # Provide detailed error message if something goes wrong
                error_msg = f"Error updating profile: {str(e)}"
                print(error_msg)  # Print to console/logs
                messages.error(request, error_msg)
        else:
            # Display form errors
            for field, errors in u_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            
            for field, errors in p_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
