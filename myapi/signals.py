from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile, CustomUser  # Adjust as necessary

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    print("Signal triggered")
    if created:
        Profile.objects.create(user=instance)
        print("Profile created")
        