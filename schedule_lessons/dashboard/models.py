from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Lesson(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)

    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_user')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_created_by', default=None)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    pending = models.BooleanField(null=False, default=True)


    def __str__(self):
        return self.name

def getDateFromDay(day):
    if day == 'Monday':
        return datetime.datetime(2018, 7, 30)
    elif day == 'Tuesday':
        return datetime.datetime(2018, 7, 31)
    elif day == 'Wednesday':
        return datetime.datetime(2018, 8, 1)
    elif day == 'Thursday':
        return datetime.datetime(2018, 8, 2)
    elif day == 'Friday':
        return datetime.datetime(2018, 8, 3)
    elif day == 'Saturday':
        return datetime.datetime(2018, 8, 4)
    elif day == 'Sunday':
        return datetime.datetime(2018, 8, 5)


class Relationship(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_user_rel')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_user_rel')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='rel_created_by', default=None, null=True)
    pending = models.BooleanField(null=False, default=True)

    def __str__(self):
        return ("Tutor: " + str(self.tutor) + " and Student: " + str(self.student))

def relationship_exists(person_one, person_two):
    try:
        Relationship.objects.get(student=person_one, tutor=person_two)
        return True
    except:
        try:
            Relationship.objects.get(student=person_two, tutor=person_one)
            return True
        except:
            return False
