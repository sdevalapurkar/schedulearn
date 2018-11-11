'''This module is used to register individual accounts models.'''
from django.contrib import admin
from .models import Profile, Availability, Skill, Notification

admin.site.register(Profile)
admin.site.register(Availability)
admin.site.register(Skill)
admin.site.register(Notification)
