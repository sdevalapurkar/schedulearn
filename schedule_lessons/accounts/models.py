from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=24, blank=False, null=False)
    bio = models.TextField(max_length=500, blank=True, null=True)
    user_type  = models.CharField(max_length=16, blank=False, null=False)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    availability = models.CharField(max_length=1000, blank=True, null=True, default='{}')
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
