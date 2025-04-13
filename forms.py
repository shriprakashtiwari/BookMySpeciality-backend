from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_type', 'booking_date', 'end_date', 'time_slot', 'guests']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.TextInput(attrs={'placeholder': 'e.g. 10:00 AM - 12:00 PM'}),
        }
