'''This module is used to create routes after /accounts/'''
from django.urls import path, include
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('personalize/', views.personalize_view, name='personalize'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('reset_password/<id>', views.reset_password, name='reset_password'),
    path('verify_email/<id>', views.verify_email, name='verify_email'),
    path('auth/', include('social_django.urls', namespace='social')),
]
