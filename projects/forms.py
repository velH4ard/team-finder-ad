"""Forms for projects app HTML views."""
from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""

    name = forms.CharField(label='Название', max_length=200)

    class Meta:
        model = Project
        fields = ('description', 'status')
        labels = {
            'description': 'Описание',
            'status': 'Статус',
        }

    def __init__(self, *args, **kwargs):
        """Sets initial title value for template compatibility."""
        super().__init__(*args, **kwargs)
        if self.instance.pk and not self.is_bound:
            self.initial['name'] = self.instance.title

    def save(self, commit=True):
        """Maps template field name to model title."""
        project = super().save(commit=False)
        project.title = self.cleaned_data['name']
        if commit:
            project.save()
            self.save_m2m()
        return project
