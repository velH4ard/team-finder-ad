"""Models for users app."""
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a profile for each new user."""
    if created:
        Profile.objects.create(user=instance)


def _get_profile(user):
    """Returns user profile if it exists."""
    if not user.pk:
        return None
    try:
        return user.profile
    except Profile.DoesNotExist:
        return None


def _get_profile_attr(user, attr_name):
    """Returns an attribute from the related profile."""
    profile = _get_profile(user)
    if profile is None:
        return None
    return getattr(profile, attr_name)


User.add_to_class('name', property(lambda user: user.first_name))
User.add_to_class('surname', property(lambda user: user.last_name))
User.add_to_class('about', property(lambda user: _get_profile_attr(user, 'description')))
User.add_to_class('avatar', property(lambda user: _get_profile_attr(user, 'avatar')))
User.add_to_class('phone', property(lambda user: _get_profile_attr(user, 'phone')))
User.add_to_class('github_url', property(lambda user: _get_profile_attr(user, 'github')))
User.add_to_class('owned_projects', property(lambda user: user.projects))
