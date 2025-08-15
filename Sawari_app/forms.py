from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'person_image', 'vehicle_type', 'capacity', 'price_per_day', 'car_image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'person_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'car_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    