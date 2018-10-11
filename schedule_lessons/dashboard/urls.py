from django.urls import path

from . import views

urlpatterns = [
    path('agenda/', views.agenda, name='agenda'),
    path('save_gcalendar_lesson/<lesson_id>', views.save_gcalendar_lesson, name='save_gcalendar_lesson'),
    path('relationships/', views.relationships, name='relationships'),
    path('search/', views.search, name='search'),
    path('profile/<user_id>/', views.public_profile, name='public_profile'), # this url is for public profiles
    path('add_student/<student_id>/', views.add_student, name='add_student'),
    path('remove_student/<student_id>/', views.remove_student, name='remove_student'),
    path('add_tutor/<tutor_id>/', views.add_tutor, name='add_tutor'),
    path('remove_tutor/<tutor_id>/', views.remove_tutor, name='remove_tutor'),
    path('schedule_lesson/', views.choose_person, name='choose_person'),
    path('schedule_lesson/<user_id>', views.schedule_lesson, name='schedule_lesson'),
    path('confirm_lesson/<lesson_id>/', views.confirm_lesson, name='confirm_lesson'),
    path('decline_lesson/<lesson_id>/', views.decline_lesson, name='decline_lesson'),
    path('reschedule_lesson/<lesson_id>/', views.reschedule_lesson, name='reschedule_lesson'),
    path('my_profile/', views.my_profile, name='my_profile'), # this url is for private profiles
    path('my_profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_profile/delete_account/', views.delete_account, name='delete_account'),
    path('my_profile/edit_availability/', views.edit_availability, name='edit_availability'),
    path('my_profile/delete_availability/<availability_id>/', views.delete_availability, name='delete_availability'),
]
