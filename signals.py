from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a new profile when a user is created
        Profile.objects.create(user=instance)
    else:
        # Update or create the profile if it doesn’t exist
        Profile.objects.update_or_create(user=instance)
