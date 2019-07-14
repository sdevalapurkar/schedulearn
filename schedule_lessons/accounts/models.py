'''Create database models.

Profile -- A model used to add more fields to a user.

Availability -- A model to model the availabily timings of users.

Skill -- Used to model the skills of a user.

Notification -- Used to model the notification sent to a user.
'''
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    '''This class models a profile with 7 fields.

    id -- The primary field of the Profile model.
    user -- A one-to-one field that is a user.
    bio -- A text field for a user's bio.
    user_type -- The user type of a user (e.g student or tutor)
    profile_pic -- The profile pic of a user.
    email_verified -- A boolean field which tells us if the user has verified
                      his email or not.
    has_signed_up -- A boolean field which tells us if it's the user's first
                     time signing up or not.
    show_tutorial -- A boolean field which tells us if have to show
                            the tutorial when they open the agenda page.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True, default='')
    user_type = models.CharField(max_length=16, blank=False, null=False)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=False, default='/default/man.png')
    email_verified = models.BooleanField(default=False)
    # the following field is useful for google sign ups
    has_signed_up = models.BooleanField(default=False)
    show_tutorial = models.BooleanField(default=True)

    def __str__(self):
        '''Used for string outputs for a profile'''
        return str(self.user.get_full_name())

class Availability(models.Model):
    '''This class models an availability with 5 fields.

    id -- The primary field of the Availability model.
    profile -- A one-to-one field that is a profile.
    day -- The name of the day (e.g Monday)
    start_time -- When the availability starts.
    end_time -- When the availability ends.
    '''
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    day = models.CharField(max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        '''Used for string outputs for an Availability'''
        return '{} from {} to {} on {}'.format(
            self.profile.user.get_full_name(), self.start_time, self.end_time,
            self.day)

class Skill(models.Model):
    '''This class models a skill with 2 fields.

    Profile -- A ForeignKey which tells us which profile the skill belongs to.
    Skill -- A charfield that tells us the actual skill.
    '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.CharField(max_length=30)

    def __str__(self):
        '''Used for string outputs for a skill'''
        return self.profile.user.get_full_name() + ' has skill: ' + self.skill

class BlockedUsers(models.Model):
    '''This class models a blocking relationship between a user blocking another
    user

    User -- The person who's blocking
    Blocked_User -- The blocked person.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rel')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_user_rel')

    def __str__(self):
        '''Used for string outputs for a blocked user'''
        return '{} blocked {}'.format(self.user.get_full_name(),
                                          self.blocked_user.get_full_name())

class Notification(models.Model):
    '''This class models a notification with 6 fields.

    user -- A one-to-one field that is a user.
    message -- A char field that holds the notification message.
    created_on -- The date the notification was created on.
    picture -- The picture of the notification.
    unread -- A boolean field which tells us if this notification is read or not
    link -- A charfield that holds the link that the user can go to if he clicks
            on the notification.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)
    created_on = models.DateTimeField()
    picture = models.ImageField(upload_to="notification_pictures", blank=True)
    unread = models.BooleanField(default=True)
    link = models.CharField(max_length=70, default='')

    def __str__(self):
        '''Used for string outputs for a notification'''
        return self.message

class Preference(models.Model):
    '''This class models a notification with 4 fields.
    id - The ID to track the preference object.
    user -- A one-to-one field that is a user.
    title -- The title of the preference.
    description -- The description of the preference.
    active -- Whether the preference is active or not.
    '''
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=150)
    active = models.BooleanField(default=True)

    @classmethod
    def create(cls, user, title, description, active):
        preference = cls(user=user, title=title, description=description,
                         active=active).save()
        return preference

# Below code is necessary
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    '''Creates a profile when a user object is created.'''
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    '''Saves a profile when a profile object is created.'''
    instance.profile.save()
