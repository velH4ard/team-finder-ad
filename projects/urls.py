"""HTML URLs for the projects application."""
from django.urls import path

from projects.web_views import (
    FavoriteProjectsView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    complete_project,
    toggle_favorite,
    toggle_participate,
)

app_name = 'projects'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('favorites/', FavoriteProjectsView.as_view(), name='favorite-projects'),
    path('create-project/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('<int:pk>/toggle-favorite/', toggle_favorite, name='toggle-favorite'),
    path('<int:pk>/toggle-participate/', toggle_participate, name='toggle-participate'),
    path('<int:pk>/complete/', complete_project, name='complete-project'),
]
