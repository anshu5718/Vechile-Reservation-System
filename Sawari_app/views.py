from django.shortcuts import render
from .models import Vehicle
def home(request):
    vehicles = Vehicle.objects.all() # Fetch all vehicles ordered by creation date
    print(vehicles)  # Debugging line to check fetched vehicles
    return render(request, 'Sawari_app/home.html', {'vehicles': vehicles})

