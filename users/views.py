from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model with custom filtering."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filters users based on query parameters."""
        queryset = super().get_queryset()
        filter_type = self.request.query_params.get('filter')
        if not filter_type or not self.request.user.is_authenticated:
            return queryset

        user = self.request.user
        if filter_type == 'fav_authors':
            return queryset.filter(projects__favorited_by__user=user).distinct()
        if filter_type == 'my_participation':
            return queryset.filter(projects__participants=user).distinct()
        if filter_type == 'likers_of_my_projects':
            return queryset.filter(projects__author=user, projects__favorited_by__isnull=False).distinct()
        if filter_type == 'participants_of_my_projects':
            return queryset.filter(projects__author=user, projects__participants__isnull=False).distinct()

        return queryset
