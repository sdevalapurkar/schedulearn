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
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout, name='logout'),
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('home/', include('scheduler.urls')),
    path('signup/', include('signup.urls')),
    path('login/', login, {'template_name': 'signup/login.html'}),
]
