'''This module is used to create routes after /api/v1/'''
from django.urls import path, include
from . import views

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('profile/<token>', views.Profile.as_view()),
    path('connections/<token>', views.Connections.as_view()),
    path('lessons/<token>', views.Lessons.as_view()),
]
