# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase

from projects.models import Project
from projects.services import ProjectService

User = get_user_model()

class ProjectServiceTests(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(
            username="david",
            email="david@example.com",
            password="password123"
        )

    def test_create_project_successfully(self):

        # Act
        project = ProjectService.create_project(
            owner=self.user,
            name="Tenski live"
        )

        # Assert
        self.assertTrue(Project.objects.filter(id=project.id).exists())
        self.assertEqual(project.owner, self.user)
        self.assertEqual(project.name, "Tenski live")
        self.assertEqual(project.slug, "tenski-live")
        self.assertEqual(project.description, "")

    def test_generates_unique_slug(self):

        project1 = ProjectService.create_project(
            owner=self.user,
            name="Conquest"
        )

        project2 = ProjectService.create_project(
            owner=self.user,
            name="Conquest"
        )

        self.assertEqual(project1.slug, "conquest")
        self.assertEqual(project2.slug, "conquest-2")
