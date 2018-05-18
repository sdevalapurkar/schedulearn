from django.urls import path

from . import views

urlpatterns = [
    path('', views.load_home),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
]
