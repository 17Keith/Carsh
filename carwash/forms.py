from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer', 'car_make', 'car_model', 'car_size']

        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-control'}),
            'car_make': forms.TextInput(attrs={'class': 'form-control'}),
            'car_model': forms.TextInput(attrs={'class': 'form-control'}),
            'car_size': forms.Select(attrs={'class': 'form-select'}),
        }
