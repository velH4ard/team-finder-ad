from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""

    class Meta:
        model = Profile
        fields = ('avatar', 'description', 'phone', 'github')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')
