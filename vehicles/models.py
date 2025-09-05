from django.db import models
from django.conf import settings
# Create your models here.
class Vehicle(models.Model):
    VEHICLE_TYPES = [('car', 'Car'), ('van', 'Van'), ('bus', 'Bus'), ('truck', 'Truck')]
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    vehicle_image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    capacity = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Active only after admin approval
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')

    # KYC fields
    citizenship_number = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50)
    kyc_submitted_at = models.DateTimeField(auto_now_add=True)
    kyc_approved = models.BooleanField(default=False)
    kyc_approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name