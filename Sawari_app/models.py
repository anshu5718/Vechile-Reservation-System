from django.db import models

# Create your models here.
class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    person_image = models.ImageField(upload_to='person_images/', blank=True, null=True)
    vehicle_type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    car_image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)

    def __str__(self):
        space = "\u00A0" * 5 
        return f"Owner name: {self.name} {space} (vechile: {self.vehicle_type}) {space}(Number of seats: {self.capacity})"
