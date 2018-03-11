from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='signup_client', permanent=False)),
    path('tutor', views.signup_tutor, name='signup_tutor'),
    path('client', views.signup_client, name='signup_client'),
]