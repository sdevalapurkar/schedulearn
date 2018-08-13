from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import Http404

class Profile(APIView):
    '''
    GET REQUEST: Returns profile information given a token.
    PUT REQUEST: Updates profile information given a token.
    '''
    def get_profile(self, token):
        try:
            token = Token.objects.get(key=token)
            return token.user.profile
        except Token.DoesNotExist:
            raise Http404

    def get(self, request, token):
        profile = self.get_profile(token)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
