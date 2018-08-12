# from django.shortcuts import render
# from rest_framework import routers, serializers, viewsets
# from .serializers import UserSerializer
# from django.contrib.auth.models import User
# from rest_framework.response import Response
from django.http import JsonResponse
# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

def get_user(request):
    user = request.user
    json = {
        'user_name': user.get_full_name(),
        'user_username': user.username,
        'user_email': user.email,
        'user_id': user.profile.id,
    }
    return JsonResponse(json)
