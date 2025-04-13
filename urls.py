# vendor/urls.py
from django.urls import path
from . import views

app_name = 'vendor'

urlpatterns = [
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('profile/', views.vendor_profile_view, name='vendor_profile'),
]
