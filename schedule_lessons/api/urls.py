from django.urls import path, include
# from api.views import UserViewSet

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
]
