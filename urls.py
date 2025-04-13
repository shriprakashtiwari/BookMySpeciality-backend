from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home

urlpatterns = [
    path('', home, name='home'),                            # Root homepage
    path('accounts/', include('accounts.urls')),            # Custom accounts views
    path('accounts/social/', include('allauth.urls')),      # Social login (Google, Facebook)
    path('admin/', admin.site.urls),                        # Django admin
    path('vendor/', include('vendor.urls')),                # Vendor dashboard and features
    path('customer/', include('customer.urls')),            # Customer dashboard and features
    path('services/', include('services.urls')),            # Services and API endpoints
    path('bookings/', include('bookings.urls')),            # Booking functionality
    path('main/', include('main.urls')),                    # Main app content
    path('api/', include('api.urls')),                      # Clean separation for API
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
