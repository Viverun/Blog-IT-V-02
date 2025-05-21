"""
URL configuration for DJANGO_PROJECT project.
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

# Simple diagnostic view
def simple_test(request):
    return HttpResponse("<h1>Email Diagnostic Tool</h1><p>This is a simple test view to verify URL routing.</p>")

# Simple email test view
def email_test(request):
    from django.core.mail import send_mail
    
    if request.GET.get('email'):
        # Try to send a test email
        try:
            recipient = request.GET.get('email')
            send_mail(
                subject='Test Email from Blog-It',
                message='This is a test email from your Django site.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            return HttpResponse(f"<h1>Test email sent to {recipient}</h1><p>Check your inbox or spam folder.</p>")
        except Exception as e:
            return HttpResponse(f"<h1>Error sending email</h1><p>Error: {str(e)}</p>")
    else:
        # Display a form
        return HttpResponse("""
            <h1>Email Test Tool</h1>
            <p>Enter your email to receive a test message:</p>
            <form method="get">
                <input type="email" name="email" required>
                <button type="submit">Send Test Email</button>
            </form>
        """)

urlpatterns = [
    # Test patterns
    path('test/', simple_test, name='simple_test'),
    path('email-test/', email_test, name='email_test'),
    
    # Admin and user management
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('user/<str:username>/', user_views.user_profile, name='user-profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', user_views.custom_logout, name='logout'),
    
    # Password reset paths
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_email_subject.txt',
             success_url='/password-reset/done/'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),
           # Include blog URLs last
    path('', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
