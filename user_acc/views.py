from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import signupForm
from django.contrib import messages
from .models import OTP, User_profile
from .utilis import is_email_valid, forgot_password_email
from django.contrib.auth.password_validation import validate_password
# Create your views here.
def first_view(request):
    return render(request,'user_acc/first.html')

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('viewer_homepage')
        else:
            return render(request, 'user_acc/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user_acc/login.html')


def signup_view(request):
    if request.method == 'POST':
        form= signupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = signupForm()
    return render(request, 'user_acc/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login_view')

def forgot_password_view(request):
    # Placeholder for forgot password logic
    if request.method == 'POST':

        email = request.POST.get('email')

        if is_email_valid(email) :
            messages.error (request, 'Enter a valid email address to reset your password')
            return redirect('forgot_password')
        try:
             forgot_password_email(email)
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'user_acc/forgot_password.html', {'error': str(e)})
        return redirect('otp_confirmation')
    return render(request, 'user_acc/forgot_password.html', {'message': 'Forgot Password functionality is not implemented yet.'})


def otp_confirmation_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = OTP.check_otp(otp)
        if user_id is None:
            messages.error(request, 'Invalid OTP')
            return render(request, 'user_acc/otp_confirmation.html', {'error': 'Invalid OTP'})  
        return redirect('set_new_password', user_id=user_id)
    return render(request, 'user_acc/otp_confirmation.html', {'message': 'OTP Confirmation functionality is not implemented yet.'})

def set_new_password_view(request, user_id= None):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('set_new_password')
        try:
            validate_password(password1)
        except Exception as e:
            for error in list(e):
                 messages.error(request, str(error))
            return render(request, 'user_acc/set_new_password.html', {'error': str(e)})
        else:
            if user_id is not None:
                user= User_profile.objects.get(id=user_id)
                if user is None:
                    messages.error(request, 'User does not exist')
                    return render(request, 'user_acc/set_new_password.html', {'error': 'User does not exist'})

            user.set_password(password1)
            user.save()
            return redirect('login_view')
        # else:
        #     messages.error(request, 'Passwords do not match')
        #     return render(request, 'user_acc/set_new_password.html', {'error': 'Passwords do not match'})
    return render(request, 'user_acc/set_new_password.html', {'message': 'Set New Password functionality is not implemented yet.'})
    

def viewer_homepage(request):
    if request.user.is_authenticated:
        return render(request, 'user_acc/viewer_homepage.html', {'username': request.user.username})
    else:
        return render(request, 'user_acc/login.html', {'error': 'You need to log in first'})