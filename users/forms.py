"""Forms for users app HTML views."""
from django import forms
from django.contrib.auth import authenticate, get_user_model

from team_finder.constants import NAME_MAX_LENGTH, SURNAME_MAX_LENGTH
from users.models import Profile

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """Registration form for a new user."""

    name = forms.CharField(label='Имя', max_length=NAME_MAX_LENGTH)
    surname = forms.CharField(label='Фамилия', max_length=SURNAME_MAX_LENGTH)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ()

    def clean_email(self):
        """Validates email uniqueness."""
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=True):
        """Creates a new user."""
        return User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['name'],
            last_name=self.cleaned_data['surname'],
            password=self.cleaned_data['password'],
        )


class EmailAuthenticationForm(forms.Form):
    """Authentication form using email and password."""

    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Введите корректные email и пароль.',
    }

    def __init__(self, request=None, *args, **kwargs):
        """Stores request for later authentication."""
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        """Authenticates the user by email."""
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').lower()
        password = cleaned_data.get('password')
        if not email or not password:
            return cleaned_data

        user = User.objects.filter(email__iexact=email).first()
        username = user.username if user else email
        self.user_cache = authenticate(
            self.request,
            username=username,
            password=password,
        )
        if self.user_cache is None:
            raise forms.ValidationError(self.error_messages['invalid_login'])
        return cleaned_data

    def get_user(self):
        """Returns the authenticated user."""
        return self.user_cache


class ProfileEditForm(forms.ModelForm):
    """Profile edit form mapped to user and profile models."""

    name = forms.CharField(label='Имя', max_length=NAME_MAX_LENGTH)
    surname = forms.CharField(label='Фамилия', max_length=SURNAME_MAX_LENGTH)
    about = forms.CharField(label='О себе', required=False, widget=forms.Textarea)
    github_url = forms.URLField(label='GitHub', required=False)

    class Meta:
        model = Profile
        fields = ('avatar', 'phone')
        labels = {
            'avatar': 'Аватар',
            'phone': 'Телефон',
        }

    def __init__(self, *args, user=None, **kwargs):
        """Fills initial values from current user and profile."""
        self.user = user
        super().__init__(*args, **kwargs)
        if user and not self.is_bound:
            self.initial.update({
                'name': user.first_name,
                'surname': user.last_name,
                'about': self.instance.description,
                'github_url': self.instance.github,
            })

    def save(self, commit=True):
        """Saves user and profile data."""
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['name']
            self.user.last_name = self.cleaned_data['surname']
            self.user.save(update_fields=['first_name', 'last_name'])
        profile.description = self.cleaned_data['about']
        profile.github = self.cleaned_data['github_url']
        if commit:
            profile.save()
        return self.user if self.user else profile
