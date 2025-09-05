from django.shortcuts import render, redirect
from .forms import VehicleRegistrationForm
from .models import Vehicle
from django.contrib import messages
from user_acc.models import User_profile
from django.contrib.auth.decorators import login_required
def register_vehicle(request):
    # request.user is already your User_profile instance
    if request.method == 'POST':
        form = VehicleRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.user_type == 'driver' or request.user.user_type == 'admin':
                vehicle = form.save(commit=False)
                vehicle.owner = request.user   # link vehicle to the logged-in driver
                vehicle.save()
                return redirect('viewer_homepage')
            else:
                return render(request, 'vehicles/registration_form.html', {
                    'form': form,
                    'error': 'Only drivers and admins can register vehicles.'
                })
    else:
        form = VehicleRegistrationForm()

    return render(request, 'vehicles/registration_form.html', {'form': form})


@login_required
def driver_homepage(request):
    if request.user.user_type != "driver":
        messages.error(request, "Only drivers can access this page.")
        return redirect("login_view")

    vehicles = Vehicle.objects.filter(
        owner=request.user,
        is_active=True,
        kyc_approved=True
    )
    return render(request, 'vehicles/driver_homepage.html', {'vehicles': vehicles})

    



