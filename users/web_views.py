"""HTML views for users app."""
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from team_finder.constants import ITEMS_PER_PAGE
from users.forms import EmailAuthenticationForm, ProfileEditForm, UserRegistrationForm
from users.models import Profile

User = get_user_model()


class RegisterView(CreateView):
    """Handles user registration."""

    form_class = UserRegistrationForm
    template_name = 'users/register.html'

    def get_success_url(self):
        """Returns redirect target after registration."""
        return reverse('users:login')


class EmailLoginView(auth_views.LoginView):
    """Logs a user in by email and password."""

    authentication_form = EmailAuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        """Returns redirect target after successful login."""
        return self.get_redirect_url() or reverse('projects:project-list')


class UserDetailView(DetailView):
    """Displays a public user profile."""

    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Allows the current user to edit their profile."""

    model = Profile
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        """Returns or creates the current user's profile."""
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        """Adds current user to template context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_success_url(self):
        """Returns redirect target after profile update."""
        return reverse('users:user-detail', kwargs={'pk': self.request.user.pk})


class UserListView(ListView):
    """Shows the list of registered users."""

    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """Returns users filtered by the selected criterion."""
        queryset = User.objects.order_by('-date_joined')
        if not self.request.user.is_authenticated:
            return queryset

        active_filter = self.request.GET.get('filter')
        if active_filter == 'owners-of-favorite-projects':
            return queryset.filter(projects__favorites__user=self.request.user).distinct()
        if active_filter == 'owners-of-participating-projects':
            return queryset.filter(projects__participants=self.request.user).distinct()
        if active_filter == 'interested-in-my-projects':
            return queryset.filter(favorites__project__author=self.request.user).distinct()
        if active_filter == 'participants-of-my-projects':
            return queryset.filter(joined_projects__author=self.request.user).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        """Adds active filter to template context."""
        context = super().get_context_data(**kwargs)
        context['active_filter'] = self.request.GET.get('filter')
        return context


class UserPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    """Allows authenticated users to change password."""

    template_name = 'users/change_password.html'
    success_url = None

    def get_success_url(self):
        """Returns redirect target after successful password change."""
        return reverse('users:user-detail', kwargs={'pk': self.request.user.pk})
