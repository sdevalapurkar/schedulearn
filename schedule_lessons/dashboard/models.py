'''Create database models.

Lesson -- The lesson model that models the items logged-on a tutor and a student
          can create between each other.

Relationship -- The relationship model that models the connection between a
                student and a tutor.
'''
from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    '''This class models a lesson with 10 fields.

    id -- The primary field of the Lesson model.
    name -- A character field that's the name of the lesson.
    description -- A character field that's the description of the lesson.
    location -- A character field that's the location that the lesson is going
                to happen in.
    tutor -- A field that contains the tutor user of the lesson.
    student -- A field that contains the student user of the lesson.
    created_by -- A field that contains the user who created the lesson.
    start_time -- A datetime field that's the starting time of the lesson.
    end_time -- A datetime field that's the ending time of the lesson.
    pending -- A boolean field that shows whether the lesson is pending or not.
    '''
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)

    tutor = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='tutor_user')
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='student_user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='lesson_created_by',
                                   default=None)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    pending = models.BooleanField(null=False, default=True)

    def __str__(self):
        '''Returns the lessons name for string printing purposes.'''
        return self.name

class Relationship(models.Model):
    '''This class models a relationship with 4 fields

    tutor -- A field that contains the tutor user of the relationship.
    student -- A field that contains the student user of the relationship.
    created_by -- A field that contains the user who created the relationship.
    pending -- A boolean field that shows whether the relationship is pending or
               not.
    '''
    tutor = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='tutor_user_rel')
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='student_user_rel')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   related_name='rel_created_by', default=None,
                                   null=True)

    pending = models.BooleanField(null=False, default=True)

    def __str__(self):
        return 'Tutor: {} and Student: {}'.format(self.tutor, self.student)
