"""schedule_lessons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

# TODO: Import views.py from the same working directory as this file.
# The above is necessary to get the method that youre going to make in views.py

# TODO: In order to make sure your error404 method is executed when someone goes
# to a page that they're not supposed to, you need to create a variable called
# error404 and make it equal to your method in views.py

urlpatterns = [
    path('', include('home.urls'), name='home'),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Needed for media folder to upload profile pictures.
