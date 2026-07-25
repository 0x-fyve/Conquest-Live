from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Competition
from .services import CompetitionService
from projects.services import ProjectService
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

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

    def test_rejects_invalid_dates(self):
        
        starts_at = timezone.now()
        ends_at = starts_at - timedelta(days=1)

        with self.assertRaises(ValidationError) as context:
            CompetitionService.create_competition(
                project=self.project,
                name="Tenski main",
                starts_at=starts_at,
                ends_at=ends_at
            )

        self.assertEqual(
            context.exception.detail["ends_at"][0],
            "End date must be after the start date."
        )