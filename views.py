from django.shortcuts import render

def customer_dashboard(request):
    return render(request, 'customer/dashboard.html')

