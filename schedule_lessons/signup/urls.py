from django.urls import path

from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('tutor', views.signup_tutor, name='signup_tutor'),
    path('client', views.signup_client, name='signup_client'),
]