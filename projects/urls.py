"""URLs for the projects application."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from projects.views import FavoriteViewSet, ProjectViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]
