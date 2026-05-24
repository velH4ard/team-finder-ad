"""HTML views for projects app."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from projects.forms import ProjectForm
from projects.models import Favorite, Project
from team_finder.constants import STATUS_CLOSED


class ProjectListView(ListView):
    """Shows the main list of projects."""

    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

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
    paginate_by = 12

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
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, View):
    """Creates a new project."""

    template_name = 'projects/create-project.html'

    def get(self, request):
        """Renders empty project form."""
        return render(request, self.template_name, {'form': ProjectForm(), 'is_edit': False})

    def post(self, request):
        """Saves a newly created project."""
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect('projects:project-detail', pk=project.pk)
        return render(request, self.template_name, {'form': form, 'is_edit': False})


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Edits an existing project."""

    template_name = 'projects/create-project.html'

    def test_func(self):
        """Allows editing only by the project author."""
        return self.get_project().author == self.request.user

    def get_project(self):
        """Returns the target project."""
        return get_object_or_404(Project, pk=self.kwargs['pk'])

    def get(self, request, pk):
        """Renders project form with initial data."""
        project = self.get_project()
        return render(
            request,
            self.template_name,
            {'form': ProjectForm(instance=project), 'is_edit': True, 'project': project},
        )

    def post(self, request, pk):
        """Saves project changes."""
        project = self.get_project()
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            return redirect('projects:project-detail', pk=project.pk)
        return render(
            request,
            self.template_name,
            {'form': form, 'is_edit': True, 'project': project},
        )


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
