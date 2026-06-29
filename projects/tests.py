from django.test import TestCase

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
            name="Zombie Wars"
        )

        # Assert
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(project.owner, user)
        self.assertEqual(project.name, "Zombie Wars")
        self.assertEqual(project.slug, "zombie-wars")