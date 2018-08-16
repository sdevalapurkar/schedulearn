from rest_framework import serializers
from accounts.models import Profile
from dashboard.models import Relationship, Lesson
from django.contrib.auth.models import User


# Serializers define the API representation.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# Serializer for Relationships
class ConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ('tutor','student')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
