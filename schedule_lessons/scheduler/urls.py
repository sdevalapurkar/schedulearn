from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_tutors', views.get_tutors, name='get_tutors'),
]