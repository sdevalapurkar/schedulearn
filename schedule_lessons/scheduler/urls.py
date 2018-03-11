from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_tutors', views.get_tutors, name='get_tutors'),
    path('get_events', views.get_events, name='get_events'),
    path('set_event', views.set_event, name='set_event'),
    path('availability/<tutor_id>', views.get_availability, name='get_availability')
]