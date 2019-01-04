'''This module is used to serialize models.'''
from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile
from dashboard.models import Relationship, Lesson
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


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

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.profile.save()
        return user
