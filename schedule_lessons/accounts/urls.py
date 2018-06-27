from django.urls import path, include
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('personalize/', views.personalize_view, name='personalize'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
]
