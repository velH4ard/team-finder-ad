"""Views for the projects application."""
from rest_framework import permissions, viewsets, status, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from projects.models import Project, Favorite
from projects.serializers import ProjectSerializer, FavoriteSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permission class to allow only authors to edit objects."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for Project model."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Sets the author of the project to the current user."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        """Allows adding/removing a project from favorites."""
        project = self.get_object()
        if request.method == 'POST':
            Favorite.objects.get_or_create(user=request.user, project=project)
            return Response({'status': 'added to favorites'},
                            status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            Favorite.objects.filter(user=request.user, project=project).delete()
            return Response({'status': 'removed from favorites'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """ViewSet for Favorite model."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Sets the user of the favorite to the current user."""
        serializer.save(user=self.request.user)
