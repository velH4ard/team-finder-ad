from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions
from .serializers import UserSerializer

User = get_user_model()


class UserFilter(filters.FilterSet):
    # Criteria:
    # 1. 'Авторы избранных проектов' (favorites__user=request.user.projects__author?)
    # Wait, simple: authors of projects that user marked as favorite
    # 'Авторы проектов, в которых я участвую'
    # 'Пользователи, которым нравятся мои проекты'
    # 'Участники моих проектов'
    
    # Custom filtering logic needed.
    # Actually, the user list filtering can be done using `get_queryset` with query params.
    pass


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.query_params.get('filter')
        if not filter_type or not self.request.user.is_authenticated:
            return queryset
        
        user = self.request.user
        if filter_type == 'fav_authors':
            return queryset.filter(projects__favorited_by__user=user).distinct()
        elif filter_type == 'my_participation':
            return queryset.filter(projects__participants=user).distinct()
        elif filter_type == 'likers_of_my_projects':
            return queryset.filter(favorites__project__author=user).distinct()
        elif filter_type == 'participants_of_my_projects':
            return queryset.filter(joined_projects__author=user).distinct()
            
        return queryset
