from django.contrib import admin
from .models import Relationship, Lesson

# Register your models here.

admin.site.register(Lesson)

admin.site.register(Relationship)
