from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



class CustomUser(AbstractUser):
    # Add custom fields here if needed
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.username

USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    )



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    brand_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    services_offered = models.TextField()
    location = models.CharField(max_length=255)
    pricing_info = models.TextField()
    phone_number = models.CharField(max_length=10)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"

# Automatically create or update Profile when User is created or saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
