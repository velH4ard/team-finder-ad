"""HTML views for users app."""
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from users.forms import EmailAuthenticationForm, ProfileEditForm, UserRegistrationForm

User = get_user_model()


class RegisterView(View):
    """Handles user registration."""

    template_name = 'users/register.html'

    def get(self, request):
        """Renders registration form."""
        return render(request, self.template_name, {'form': UserRegistrationForm()})

    def post(self, request):
        """Creates a new user when form is valid."""
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        return render(request, self.template_name, {'form': form})


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


class EditProfileView(LoginRequiredMixin, View):
    """Allows the current user to edit their profile."""

    template_name = 'users/edit_profile.html'

    def get(self, request):
        """Renders profile edit form."""
        form = ProfileEditForm(user=request.user)
        return render(request, self.template_name, {'form': form, 'user': request.user})

    def post(self, request):
        """Updates current user profile."""
        form = ProfileEditForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user-detail', pk=request.user.pk)
        return render(request, self.template_name, {'form': form, 'user': request.user})


class UserListView(ListView):
    """Shows the list of registered users."""

    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = 12

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
