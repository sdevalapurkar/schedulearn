'''This module is used to create routes after /'''

from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_home, name='home'),
    path('privacy_policy/', views.load_privacy_policy, name='privacy_policy')
]
