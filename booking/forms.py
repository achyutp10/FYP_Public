from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['email', 'name', 'address', 'phone_number']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }
