# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase

from projects.models import Project
from projects.services import ProjectService

User = get_user_model()

class ProjectServiceTests(TestCase):

    def test_create_project_successfully(self):
        # Arrange
        user = User.objects.create_user(
            username="david",
            email="david@example.com",
            password="password123"
        )

        # Act
        project = ProjectService.create_project(
            owner=user,
            name="Tenski live"
        )

        # Assert
        self.assertTrue(Project.objects.filter(id=project.id).exists())
        self.assertEqual(project.owner, user)
        self.assertEqual(project.name, "Tenski live")
        self.assertEqual(project.slug, "tenski-live")
        self.assertEqual(project.description, "")

    def test_generates_unique_slug(self):

        user = User.objects.create_user(
            username="david",
            email="david@example.com",
            password="password123"
        )

        project1 = ProjectService.create_project(
            owner=user,
            name="Conquest"
        )

        project2 = ProjectService.create_project(
            owner=user,
            name="Conquest"
        )

        self.assertEqual(project1.slug, "conquest")
        self.assertEqual(project2.slug, "conquest-2")
