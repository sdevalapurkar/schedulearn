from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True, default='')
    user_type  = models.CharField(max_length=16, blank=False, null=False)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_verified = models.BooleanField(default=False)
    has_signed_up = models.BooleanField(default=False) # this is useful for google sign ups

    def __str__(self):
        return str(self.user)

class Availability(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    day = models.CharField(max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.profile.user.get_full_name() + ' from ' + str(self.start_time) + ' to ' + str(self.end_time) + ' on ' + self.day

# Will return a list of availabilities (dictionary) of the profile id, sorted by order Monday To Sunday.
def return_availabilities(user_id):
    availabilities = []
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days_of_the_week:
        availabilities_in_day = Availability.objects.filter(profile__id=user_id, day=day)
        if availabilities_in_day:
            for availability_in_day in availabilities_in_day:
                availabilities.append(availability_in_day)

    return availabilities
    
# Below code is necessary
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
