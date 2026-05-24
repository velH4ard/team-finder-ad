"""Admin configuration for projects app."""
from django.contrib import admin

from projects.models import Favorite, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Project model."""
    list_display = ('title', 'author', 'status', 'pub_date')
    search_fields = ('title', 'author__username')
    list_filter = ('status', 'pub_date')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin configuration for Favorite model."""
    list_display = ('user', 'project')
    search_fields = ('user__username', 'project__title')
    list_filter = ('user',)
