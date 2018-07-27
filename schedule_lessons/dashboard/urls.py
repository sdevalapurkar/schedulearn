from django.urls import path

from . import views

urlpatterns = [
    path('agenda/', views.agenda, name='agenda'),
    path('relationships/', views.relationships, name='relationships'),
    path('search/', views.search, name='search'),
    path('profile/<id>/', views.public_profile, name='public_profile'), # this url is for public profiles
    path('my_profile/', views.my_profile, name='my_profile'), # this url is for private profiles
    path('edit_profile/', views.edit_profile, name='edit_profile'), # this url is for private profiles
    path('add_student/<id>/', views.add_student, name='add_student'),
    path('remove_student/<id>/', views.remove_student, name='remove_student'),
    path('add_tutor/<id>/', views.add_tutor, name='add_tutor'),
    path('remove_tutor/<id>/', views.remove_tutor, name='remove_tutor'),
    path('get_profile_pic/', views.get_profile_pic, name='get_profile_pic'),
]
