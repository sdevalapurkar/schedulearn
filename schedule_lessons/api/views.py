from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import Http404
from dashboard.models import Relationship, Lesson
from .serializers import ProfileSerializer, LessonSerializer

class Profile(APIView):
    '''
    GET REQUEST: Returns profile info (bio, user_type,
                 path to profile pic) given an auth token.
    PUT REQUEST: Updates profile info (bio, user_type, path to profile pic)
                 given a token and data.
    '''

    def get(self, request, token):
        '''GET REQUEST: Returns profile info (bio,
                        user_type, path to profile pic) given an auth token.
        '''
        profile = get_profile(token)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, token):
        '''PUT REQUEST: Updates profile info (bio, user_type,
                        path to profile pic) given a token and data.
        '''
        profile = get_profile(token)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class Lessons(APIView):
    '''GET REQUEST: Returns all lessons given a token.'''
    def get(self, request, token):
        '''GET REQUEST: Returns all lessons given a token.'''
        user = get_user(token)
        lessons = []
        if user.profile.user_type == 'tutor':
            lessons_db = Lesson.objects.filter(tutor=user)
        else:
            lessons_db = Lesson.objects.filter(student=user)
        for lesson in lessons_db:
            serializer = LessonSerializer(lesson)
            data = serializer.data
            data['lesson_with'] = (lesson.tutor.get_full_name() if
                                   user.profile.user_type == 'student' else
                                   lesson.student.get_full_name())
            lessons.append(data)
        return Response({'lessons': lessons})

class Connections(APIView):
    '''GET REQUEST: Returns all connections given a token.'''

    def get(self, request, token):
        '''GET REQUEST: Returns all connections given a token.'''
        user = get_user(token)
        connections = []
        relationships = (Relationship.objects.filter(tutor=user) if
                         user.profile.user_type == 'tutor' else
                         Relationship.objects.filter(student=user))
        for relationship in relationships:
            if user.profile.user_type == 'tutor':
                profile_serializer = ProfileSerializer(
                    relationship.student.profile)
                person_info = profile_serializer.data
                person_info['first_name'] = relationship.student.first_name
                person_info['last_name'] = relationship.student.last_name
            else:
                profile_serializer = ProfileSerializer(
                    relationship.tutor.profile)
                person_info = profile_serializer.data
                person_info['first_name'] = relationship.tutor.first_name
                person_info['last_name'] = relationship.tutor.last_name

            connections.append(person_info)

        return Response({'connections': connections})

# Helper Functions

def get_profile(token):
    '''Returns a profile object given a token, if no profile, raises error.
    '''
    try:
        token = Token.objects.get(key=token)
        return token.user.profile
    except Token.DoesNotExist:
        raise Http404

def get_user(token):
    '''Returns a user object given a token, if no user, raises error.'''
    try:
        token = Token.objects.get(key=token)
        return token.user
    except Token.DoesNotExist:
        raise Http404

# Future API Developments will need to branch into interacting with individual
# lessons (GET, POST, PUT, DELETE), interacting with the availabilities of
# users, and creating new connections between users (POST)
