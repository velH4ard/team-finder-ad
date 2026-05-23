"""Models for the projects application."""
from django.contrib.auth import get_user_model
from django.db import models

from team_finder.constants import STATUS_CHOICES, STATUS_OPEN, TITLE_MAX_LENGTH, STATUS_MAX_LENGTH

User = get_user_model()


class Project(models.Model):
    """Represents a project on the platform."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
        verbose_name='Статус'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    participants = models.ManyToManyField(
        User,
        related_name='joined_projects',
        blank=True,
        verbose_name='Участники'
    )

    class Meta:
        """Meta options for Project model."""
        ordering = ('-pub_date',)
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        """Returns the project title."""
        return self.title


class Favorite(models.Model):
    """Represents a favorite project for a user."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Проект'
    )

    class Meta:
        """Meta options for Favorite model."""
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'],
                name='unique_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        """Returns string representation of favorite."""
        return f'{self.user.username} - {self.project.title}'
