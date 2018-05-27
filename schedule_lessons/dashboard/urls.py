from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('get_tutors', views.get_tutors, name='get_tutors'),
    path('get_events', views.get_events, name='get_events'),
    path('set_event', views.set_event, name='set_event'),
    path('scheduler', views.scheduler, name='scheduler'),
    path('availability/<tutor_id>', views.get_availability, name='get_availability'),
    path('edit_availability', views.edit_availability, name='edit_availability'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('my_profile/edit_profile_pic/', views.edit_profile_pic, name='edit_profile_pic'),
    path('user_type', views.user_type, name='user_type'),
    path('add_tutor', views.add_tutor, name='add_tutor'),
    path('confirm_lesson', views.confirm_lesson, name='confirm_lesson'),
    path('decline_lesson', views.decline_lesson, name='decline_lesson'),
]
