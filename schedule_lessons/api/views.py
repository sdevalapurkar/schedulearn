from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import Http404
from dashboard.models import Relationship, Lesson

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

class Lessons(APIView):
    '''
    GET REQUEST: Returns lessons given a token.
    PUT REQUEST: Updates a lesson given a token.
    POST REQUEST: Adds a lesson given a token.
    '''
    def get_user(self, token):
        try:
            token = Token.objects.get(key=token)
            return token.user
        except Token.DoesNotExist:
            raise Http404

    def get(self, request, token):
        user = self.get_user(token)
        lessons = []
        if user.profile.user_type == 'tutor':
            lessons_db = Lesson.objects.filter(tutor=user)
        else:
            lessons_db = Lesson.objects.filter(student=user)
        for lesson in lessons_db:
            serializer = LessonSerializer(lesson)
            data = serializer.data
            data['lesson_with'] = lesson.tutor.get_full_name() if user.profile.user_type == 'student' else lesson.student.get_full_name()
            lessons.append(data)
        return Response({'lessons': lessons})

class Connections(APIView):
    '''
    GET REQUEST: Returns all connections given a token.
    POST REQUEST: Add a connection given a token.
    '''
    def get_user(self, token):
        try:
            token = Token.objects.get(key=token)
            return token.user
        except Token.DoesNotExist:
            raise Http404

    def get(self, request, token):
        user = self.get_user(token)
        connections = []
        relationships = Relationship.objects.filter(tutor=user) if user.profile.user_type == 'tutor' else Relationship.objects.filter(student=user)
        for relationship in relationships:
            if user.profile.user_type == 'tutor':
                profile_serializer = ProfileSerializer(relationship.student.profile)
                person_info = profile_serializer.data
                person_info['first_name'] = relationship.student.first_name
                person_info['last_name'] = relationship.student.last_name
            else:
                profile_serializer = ProfileSerializer(relationship.tutor.profile)
                person_info = profile_serializer.data
                person_info['first_name'] = relationship.tutor.first_name
                person_info['last_name'] = relationship.tutor.last_name

            connections.append(person_info)

        return Response({'connections': connections})
