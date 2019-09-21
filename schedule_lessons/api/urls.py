'''This module is used to create routes after /api/v1/'''
from django.urls import path, include, re_path
from . import views
from allauth.account.views import confirm_email
from .adapters import facebook_login, google_login

urlpatterns = [
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email, name="account_confirm_email"),
    path('rest-auth/facebook/', facebook_login, name='fb_connect'),
    path('rest-auth/google/', google_login, name='google_login'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('profile/<token>/', views.Profile.as_view()),
    path('connections/<token>/', views.Connections.as_view()),
    path('lessons/<token>/', views.Lessons.as_view()),
]
