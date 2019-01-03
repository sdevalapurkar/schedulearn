'''This module is used to create routes after /accounts/'''
from django.urls import path, include
from . import views
from allauth.account.views import logout, email, login, signup
urlpatterns = [
    path('signup/', signup, name='account_signup'),
    path('personalize/', views.personalize_view, name='personalize'),
    path('login/', login, name='account_login'),
    path('logout/', logout, name='account_logout'),
    path('email/', email, name='account_email'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('reset_password/', views.reset_password, name='account_reset_password'),
    path('verify_email/<user_id>', views.verify_email, name='verify_email'),
    path('auth/', include('social_django.urls', namespace='social')),
]
