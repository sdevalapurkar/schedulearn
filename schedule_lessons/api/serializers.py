'''This module is used to serialize models.'''
from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile
from dashboard.models import Relationship, Lesson


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    '''This class serializes the User model.'''
    class Meta:
        '''This class serializes by adding all fields of the User model.'''
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    '''This class serializes the Profile model.'''
    class Meta:
        '''This class serializes by adding only the bio, user_type, and the pfp
            of the profile model.
        '''
        model = Profile
        fields = ('bio', 'user_type', 'profile_pic')

# Serializer for Relationships
class ConnectionsSerializer(serializers.ModelSerializer):
    '''This class serializes the Relationship model.'''
    class Meta:
        '''This class serializes by adding only the tutor and user field of the
           relationship model.
        '''
        model = Relationship
        fields = ('tutor', 'student')

class LessonSerializer(serializers.ModelSerializer):
    '''This class serializes the Lesson model.'''
    class Meta:
        '''This class serializes by adding all fields of the Lesson model.'''
        model = Lesson
        fields = '__all__'
