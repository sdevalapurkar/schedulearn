from django.contrib import admin
from .models import Profile, Availability, Skill

# Register your models here.

admin.site.register(Profile)
admin.site.register(Availability)
admin.site.register(Skill)
