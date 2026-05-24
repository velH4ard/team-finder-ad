from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from projects.web_views import ProjectListView

urlpatterns = [
    path('', ProjectListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),
    path('api/v1/', include('projects.api_urls')),
    path('api/v1/users/', include('users.api_urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
