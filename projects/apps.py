"""Apps configuration for projects app."""
from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """Configuration for Projects app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'
    verbose_name = 'Проекты'
