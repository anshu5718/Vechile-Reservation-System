def is_email_valid(email):
	if email == '' or email is None or '@' not in email:
		return True
	return False



def forgot_password_email(email):
	from django.core.mail import send_mail
	from django.conf import settings
	from .models import OTP
	subject = 'Password Reset Request'
	message = f'Use {OTP.otp_generator(email)} to reset your password.'
	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
	
