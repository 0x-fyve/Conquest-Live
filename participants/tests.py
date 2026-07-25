from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Participant
from .services import ParticipantService
from projects.services import ProjectService
from competitions.services import CompetitionService

User = get_user_model()

# Create your tests here.
class ParticipantServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="david",
            email="david@example.com",
            password="password123"
        )

        self.project = ProjectService.create_project(
            owner=self.user,
            name="Conquest"
        )
        self.competition = CompetitionService.create_competition(
            project=self.project,
            name="Season 1"
        )

        self.metadata = {
            "avatar": "xxxxx"
        }
        self.external_id = "ex-1"
        self.display_name ="david"
        
        self.participant = ParticipantService.create_or_update_participant(
                    external_id = self.external_id,
                    display_name =self.display_name,
                    competition = self.competition,
                    metadata= self.metadata

                )

    def test_create_new_participant(self):

        self.assertTrue(Participant.objects.filter(id=self.participant.id).exists())
        self.assertEqual(Participant.objects.count(), 1)
        self.assertEqual(self.participant.external_id, self.external_id)
        self.assertEqual(self.participant.display_name, self.display_name)
        self.assertEqual(self.participant.competition, self.competition)
        self.assertEqual(self.participant.metadata, self.metadata)

    def test_updates_existing_participant(self):
        new_display_name = "dave"
        new_metadata = {
            "avatar": "yyyyy"
        }

        updated_participant = ParticipantService.create_or_update_participant(
            external_id=self.external_id,
            display_name=new_display_name,
            competition=self.competition,
            metadata=new_metadata
        )
        updated_participant.refresh_from_db()

        self.assertEqual(Participant.objects.count(), 1)
        self.assertEqual(updated_participant.id, self.participant.id)
        self.assertEqual(updated_participant.display_name, new_display_name)
        self.assertEqual(updated_participant.metadata, new_metadata)
        self.assertEqual(updated_participant.external_id, self.external_id)
        self.assertEqual(updated_participant.competition, self.competition)


    
    