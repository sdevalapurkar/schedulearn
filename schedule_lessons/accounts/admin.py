'''This module is used to register individual accounts models.'''
from django.contrib import admin
from .models import Profile, Availability, Skill, Notification, BlockedUsers


admin.site.register(Availability)
admin.site.register(BlockedUsers)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(Skill)
