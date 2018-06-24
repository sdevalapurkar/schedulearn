from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)

    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_user')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_user')

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    pending = models.BooleanField(null=False, default=True)


    def __str__(self):
        return self.name


class Relationship(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_user_rel')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_user_rel')
