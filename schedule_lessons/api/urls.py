from django.urls import path, include
# from api.views import UserViewSet
from .views import *

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('profile/<token>', Profile.as_view()),
    path('connections/<token>', Connections.as_view()),
    path('lessons/<token>', Lessons.as_view()),
]