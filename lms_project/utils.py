import os
from django.core.mail import send_mail
from django.conf import settings

def send_lms_email(subject, message, recipient_list):
    """
    Standard wrapper for sending emails. 
    In development, this will print to the console if EMAIL_BACKEND is 'console'.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False
