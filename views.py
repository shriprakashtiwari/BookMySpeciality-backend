from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking
from services.models import Service
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service
            booking.save()
            return redirect('booking_success')  # or any success page
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'service': service,
    })

@login_required
def booking_list(request):
    if request.user.is_staff:
        bookings = Booking.objects.all()
    else:
        bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

def booking_success(request):
    return HttpResponse("<h2>Booking Successful!</h2><p>Your request has been submitted.</p>")

