"""Serializers for the projects application."""
from rest_framework import serializers

from projects.models import Favorite, Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model."""

    class Meta:
        model = Project
        fields = ('id', 'author', 'title', 'description', 'status', 'pub_date', 'participants')
        read_only_fields = ('author', 'pub_date')


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorite model."""

    class Meta:
        model = Favorite
        fields = ('user', 'project')
        read_only_fields = ('user',)
