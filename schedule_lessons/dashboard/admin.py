'''This module is used to register individual dashboard models.'''
from django.contrib import admin
from .models import Relationship, Lesson


admin.site.register(Lesson)
admin.site.register(Relationship)
