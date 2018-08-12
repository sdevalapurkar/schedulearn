from django.urls import path, include
# from api.views import UserViewSet
from .views import get_user

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('get_user/', get_user)
]
