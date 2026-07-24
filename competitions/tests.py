from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Competition
from .services import CompetitionService
from projects.services import ProjectService

User = get_user_model()

# Create your tests here.
class CompetitionServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="david",
            email="david@example.com",
            password="password123"
        )

        self.project = ProjectService.create_project(
            owner=self.user,
            name="Tenski live"
        )

    def test_create_competition_successfully(self):
        competition = CompetitionService.create_competition(
            project=self.project,
            name="Tenski main"
        )   

        self.assertTrue(Competition.objects.filter(id=competition.id).exists())
        self.assertEqual(competition.project, self.project)
        self.assertEqual(competition.name, "Tenski main")
        self.assertEqual(competition.slug,"tenski-main" )
        self.assertEqual(competition.description, "")
        self.assertEqual(competition.rules, {})
        self.assertEqual(competition.status, "DRAFT")