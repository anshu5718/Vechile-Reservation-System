from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.conf import settings
from vehicles.models import Vehicle

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('available', 'available'),
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('completed', 'completed'),
        
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    purpose = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    payment_status = models.CharField(max_length=20 , default='Unpaid')
    
    def can_user_cancel(self):
        """User can cancel if more than 2 days remain."""
        return timezone.now().date() <= self.start_date - timedelta(days=2)

    def can_owner_cancel(self):
        """Owner can cancel if more than 5 days remain."""
        return timezone.now().date() <= self.start_date - timedelta(days=5)