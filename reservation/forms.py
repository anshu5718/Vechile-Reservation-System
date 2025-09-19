from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'purpose']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-1/4 px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-1/4 px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'w-1/2 h-32 px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter purpose of reservation...'
            }),
        }
