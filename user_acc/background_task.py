from background_task import background
from django.core.mail import send_mail
from django.conf import settings

@background(schedule=3)
def send_otp(email, new_otp):
    subject = 'Password Reset Request'
    message = f'Use {new_otp} to reset your password.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    print('OTP sent successfully')
	
