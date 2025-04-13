from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:service_id>/', views.create_booking, name='create_booking'),
    path('list/', views.booking_list, name='booking_list'),
    path('success/', views.booking_success, name='booking_success'),
]

