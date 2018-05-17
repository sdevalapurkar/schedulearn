from django.contrib import admin
from .models import Relationships, Events

# Register your models here.

admin.site.register(Events)

admin.site.register(Relationships)
