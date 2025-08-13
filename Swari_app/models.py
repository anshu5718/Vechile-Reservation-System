from django.db import models

# Create your models here.
class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.vehicle_type}) - Capacity: {self.capacity}, Price: {self.price_per_day}"
