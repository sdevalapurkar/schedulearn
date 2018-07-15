from django.urls import path

from . import views

urlpatterns = [
    path('', views.scheduler, name='scheduler'),
    path('get_tutors', views.get_tutors, name='get_tutors'),
    path('get_events', views.get_events, name='get_events'),
    path('set_event', views.set_event, name='set_event'),
    path('availability/<tutor_id>', views.get_availability, name='get_availability'),
    path('edit_availability', views.edit_availability, name='edit_availability'),
    path('profile/<id>', views.public_profile, name='public_profile'), # this url is for public profiles
    path('my_profile', views.my_profile, name='my_profile'), # this url is for private profiles
    path('edit_profile/', views.edit_profile, name='edit_profile'), # this url is for private profiles
    path('user_type', views.user_type, name='user_type'),
    path('scheduler/add_tutor/', views.add_tutor, name='add_tutor'),
    path('confirm_lesson', views.confirm_lesson, name='confirm_lesson'),
    path('decline_lesson', views.decline_lesson, name='decline_lesson'),
]
