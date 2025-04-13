from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def vendor_dashboard(request):
    return render(request, 'vendor/dashboard.html')

@login_required
def vendor_profile_view(request):
    return render(request, 'vendor/profile.html')
