from rest_framework import serializers
from accounts.models import Profile

# Serializers define the API representation.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
