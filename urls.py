from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import home

urlpatterns = [
    path('', home, name='home'),                      # ✅ Only one home view here
    path('accounts/', include('allauth.urls')),       # Google/Facebook login
    path('admin/', admin.site.urls),                  # Django admin
    path('vendor/', include('vendor.urls')),          # Vendor app routes
    path('customer/', include('customer.urls')),      # Customer app
    path('services/', include('services.urls')),      # Services app
    path('bookings/', include('bookings.urls')),      # Booking system
    path('api/services/', include('services.urls')),  # Optional API
    path('main/', include('main.urls')),              # Moved to /main
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
