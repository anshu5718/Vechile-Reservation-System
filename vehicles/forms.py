from django import forms
from .models import Vehicle

class VehicleRegistrationForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'name',
            'vehicle_type',
            'capacity',
            'registration_number',
            'description',
            'citizenship_number',
            'license_number',
            'vehicle_image',
            'qr_image',
            'cost_per_day',
        ]
