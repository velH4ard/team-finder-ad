"""Admin configuration for users app."""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    """Inline profile for UserAdmin."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for User model."""
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
