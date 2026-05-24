"""API URLs for the users application."""
from django.urls import path

from users.views import UserViewSet

urlpatterns = [
    path('list/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
]
