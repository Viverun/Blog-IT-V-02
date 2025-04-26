"""
Script to test Gmail SMTP connection.
"""
import os
import sys
import django
import socket
import smtplib
from email.mime.text import MIMEText

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_PROJECT.settings')
django.setup()

# Import Django components
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend

def test_connection():
    """Test connection to Gmail SMTP server."""
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    username = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    use_tls = settings.EMAIL_USE_TLS
    
    print(f"Testing connection to {host}:{port}...")
    print(f"Username: {username}")
    print(f"TLS enabled: {use_tls}")
    
    # Test basic socket connection
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✅ Socket connection successful")
        else:
            print(f"❌ Failed to connect to {host}:{port}")
            return
    except Exception as e:
        print(f"❌ Socket connection error: {str(e)}")
        return
    
    # Test SMTP authentication
    try:
        server = smtplib.SMTP(host, port)
        server.set_debuglevel(1)  # Show detailed logs
        
        if use_tls:
            server.starttls()
            print("✅ TLS connection established")
        
        server.login(username, password)
        print("✅ SMTP authentication successful")
        
        # Try to send a test email if recipient specified
        if len(sys.argv) > 1:
            recipient = sys.argv[1]
            print(f"Sending test email to {recipient}...")
            
            msg = MIMEText("This is a test email from your Django application.")
            msg['Subject'] = "Test Email from Gmail SMTP Test"
            msg['From'] = username
            msg['To'] = recipient
            
            server.send_message(msg)
            print("✅ Test email sent successfully!")
        
        server.quit()
        
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP authentication failed - incorrect username or password")
    except Exception as e:
        print(f"❌ SMTP error: {str(e)}")

if __name__ == "__main__":
    test_connection()
    if len(sys.argv) <= 1:
        print("\nTip: Add your email as an argument to send a test message:")
        print("python test_gmail.py your_email@example.com") 