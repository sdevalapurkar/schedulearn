from django.urls import path

from . import views

urlpatterns = [
    path('', views.load_home),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
