from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class TestProjectAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.project = Project.objects.create(author=self.user, title='Test Project', description='Description')

    def test_project_list(self):
        response = self.client.get('/api/v1/projects/')
        self.assertEqual(response.status_code, 200)
