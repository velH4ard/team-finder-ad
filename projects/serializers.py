from rest_framework import serializers
from projects.models import Project, Favorite

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'author', 'title', 'description', 'status', 'pub_date', 'participants')
        read_only_fields = ('author', 'pub_date')

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'project')
        read_only_fields = ('user',)
