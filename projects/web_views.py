"""HTML views for projects app."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from projects.forms import ProjectForm
from projects.models import Favorite, Project
from team_finder.constants import ITEMS_PER_PAGE, STATUS_CLOSED


class ProjectListView(ListView):
    """Shows the main list of projects."""

    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """Returns projects ordered by publication date."""
        return Project.objects.select_related('author').prefetch_related('participants').order_by('-pub_date')

    def get_context_data(self, **kwargs):
        """Adds favorite ids for the current user."""
        context = super().get_context_data(**kwargs)
        context['favorite_project_ids'] = set()
        if self.request.user.is_authenticated:
            context['favorite_project_ids'] = set(
                Favorite.objects.filter(user=self.request.user).values_list('project_id', flat=True)
            )
        return context


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    """Shows the current user's favorite projects."""

    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """Returns favorite projects for current user."""
        return Project.objects.filter(favorites__user=self.request.user).select_related('author').distinct()

    def get_context_data(self, **kwargs):
        """Adds favorite ids for the current user."""
        context = super().get_context_data(**kwargs)
        context['favorite_project_ids'] = set(
            Favorite.objects.filter(user=self.request.user).values_list('project_id', flat=True)
        )
        return context


class ProjectDetailView(DetailView):
    """Displays project details."""

    model = Project
    template_name = 'projects/project-details.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Creates a new project."""

    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        """Adds is_edit flag for template."""
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        """Sets the current user as project author."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edits an existing project."""

    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def test_func(self):
        """Allows editing only by the project author."""
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        """Adds is_edit flag for template."""
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


@login_required
@require_POST
def toggle_favorite(request, pk):
    """Adds or removes a project from favorites."""
    project = get_object_or_404(Project, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, project=project)
    if not created:
        favorite.delete()
    return JsonResponse({'status': 'ok', 'favorite': created})


@login_required
@require_POST
def toggle_participate(request, pk):
    """Adds or removes current user from project participants."""
    project = get_object_or_404(Project, pk=pk)
    if project.author == request.user:
        return JsonResponse({'status': 'error'}, status=400)

    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({'status': 'ok', 'participant': not is_participant})


@login_required
@require_POST
def complete_project(request, pk):
    """Marks a project as completed."""
    project = get_object_or_404(Project, pk=pk, author=request.user)
    project.status = STATUS_CLOSED
    project.save(update_fields=['status'])
    return JsonResponse({'status': 'ok'})
