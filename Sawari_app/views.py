from django.shortcuts import render,redirect
from .models import Vehicle
from .forms import VehicleForm
def home(request):
    vehicles = Vehicle.objects.all() # Fetch all vehicles ordered by creation date
    print(vehicles)  # Debugging line to check fetched vehicles
    return render(request, 'Sawari_app/home.html', {'vehicles': vehicles})

def vehicle_listing(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the vehicle instance
            return redirect('home')  # Redirect to home after saving
    else:
        form = VehicleForm()  # Create a new form instance
    return render(request, 'Sawari_app/vehicle_listing.html', {'form': form})
def vehicle_detail(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)  # Fetch the vehicle by ID
    return render(request, 'Sawari_app/vehicle_detail.html', {'vehicle': vehicle})


    