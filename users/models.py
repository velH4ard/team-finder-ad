"""Models for users app."""
from django.contrib.auth import get_user_model
from django.db import models

from team_finder.constants import PHONE_MAX_LENGTH

User = get_user_model()


class Profile(models.Model):
    """Represents a profile of a user."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    description = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        blank=True,
        verbose_name='Телефон'
    )
    github = models.URLField(
        blank=True,
        verbose_name='GitHub'
    )

    class Meta:
        """Meta options for Profile model."""
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        """Returns string representation of profile."""
        return f'Профиль {self.user.username}'
