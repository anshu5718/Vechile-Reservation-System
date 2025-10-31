from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import signupForm
from django.contrib import messages
from .models import OTP, User_profile
from .utilis import is_email_valid, forgot_password_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from vehicles.models import Vehicle
from reservation.models import Reservation
def first_view(request):
    return render(request,'user_acc/first.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.user_type == "customer":
                return redirect("viewer_homepage")
            elif user.user_type == "driver":
                return redirect("vehicles:driver_homepage")
            else:
                messages.error(request, "Unauthorized user type.")
                return redirect("login_view")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, 'user_acc/login.html', {'error': 'Invalid credentials'})
    
    # Handle GET requests
    return render(request, 'user_acc/login.html')  # <--- was missing


def signup_view(request):
    if request.method == 'POST':
        form= signupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = signupForm()
        messages.error (request, 'Please correct the error below.')
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
        messages.success(request, 'OTP sent successfully')
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
    
@login_required
def viewer_homepage(request):
    if request.user.user_type != "customer":
        messages.error(request, "Only customers can access this page.")
        return redirect("login_view")

    vehicles = Vehicle.objects.filter(is_active=True, kyc_approved=True)
    reservations= Reservation.objects.filter(user=request.user)
    
    return render(
        request,
        'user_acc/viewer_homepage.html',
        {
            'vehicles': vehicles,
            'reservations': reservations,
        }
    )


@login_required
def booking_cancel(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        if reservation.can_user_cancel() and reservation.status in ['pending', 'approved']:
            reservation.status = "cancelled"
            reservation.save()

            # Notify user
            send_mail(
                subject='Booking Cancelled',
                message=f'Your booking for {reservation.vehicle} has been cancelled successfully.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reservation.user.email],
            )

            # Notify owner
            send_mail(
                subject='Booking Cancelled by User',
                message=f'The booking for your vehicle {reservation.vehicle} has been cancelled by the user.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reservation.vehicle.owner.email],
            )

            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'You cannot cancel this booking anymore.')

        return redirect('viewer_homepage')

    # If GET request, render confirmation page
    return render(request, 'user_acc/booking_cancel.html', {"reservation": reservation})


