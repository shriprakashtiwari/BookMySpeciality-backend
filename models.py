from django.db import models
from django.contrib.auth import get_user_model
from services.models import Service

CustomUser = get_user_model()  # Properly set CustomUser

class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    booking_type_choices = [
        ('single', 'Single Day'),
        ('range', 'Date Range')
    ]
    booking_type = models.CharField(max_length=10, choices=booking_type_choices, default='single')

    booking_date = models.DateField()  # For single day bookings
    end_date = models.DateField(null=True, blank=True)  # For date range bookings
    time_slot = models.CharField(max_length=50)
    guests = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.service.name} ({self.booking_date})"
