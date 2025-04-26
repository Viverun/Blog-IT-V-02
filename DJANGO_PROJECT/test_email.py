"""
Standalone script to test email sending in Django.
Run with: python test_email.py your_email@example.com
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_PROJECT.settings')
django.setup()

# Import Django components
from django.core.mail import send_mail
from django.conf import settings

def test_email(recipient):
    """Send a test email to the specified recipient."""
    print(f"Sending test email to {recipient}...")
    print(f"Using email backend: {settings.EMAIL_BACKEND}")
    
    try:
        result = send_mail(
            subject='Test Email from Blog-It',
            message='This is a test email from your Django site.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        if result:
            print("Email sent successfully!")
        else:
            print("Failed to send email - no error but result was 0")
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_email(sys.argv[1])
    else:
        print("Usage: python test_email.py your_email@example.com") 