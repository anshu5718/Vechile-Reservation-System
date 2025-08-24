from .background_task import send_otp

def is_email_valid(email):
	if email == '' or email is None or '@' not in email:
		return True
	return False



def forgot_password_email(email):
	
	from .models import OTP
	
	try:
		new_otp = OTP.otp_generator(email)
	except Exception as e:
		raise Exception(str(e))
	send_otp(email, new_otp.otp)
	