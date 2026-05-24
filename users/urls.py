"""HTML URLs for the users application."""
from django.contrib.auth import views as auth_views
from django.urls import path

from users.web_views import (
    EditProfileView,
    EmailLoginView,
    RegisterView,
    UserDetailView,
    UserListView,
    UserPasswordChangeView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='projects:project-list'), name='logout'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('change-password/', UserPasswordChangeView.as_view(), name='change-password'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
