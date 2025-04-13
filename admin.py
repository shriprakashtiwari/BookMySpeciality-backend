from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()

# Optional: Unregister if already registered
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

# Register the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass  # You can add customization later if needed
