from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.services import ProjectService
from competitions.services import CompetitionService
from participants.services import ParticipantService
from .services import ScoreEventService
from.models import ScoreEvent
from rest_framework.exceptions import ValidationError
import uuid

User = get_user_model()
# Create your tests here.

class ScoreEventServiceTests(TestCase):
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
    
        self.participant = ParticipantService.create_or_update_participant(
            external_id = "ex-1",
            display_name ="david",
            competition = self.competition,
        )

        self.event_id = "5068b43e-4194-4f39-93f1-76fffe84a682"
        self.points = 10
        self.reason = "Good performance"

        self.scoreevent = ScoreEventService.record_score(
            event_id = self.event_id,
            competition = self.competition,
            participant = self.participant,
            points = self.points,
            reason = self.reason,
        )

    def test_record_score_event_successfully(self):
        self.assertEqual(ScoreEvent.objects.count(), 1)
        self.assertTrue(ScoreEvent.objects.filter(id=self.scoreevent.id).exists())
        self.assertEqual(self.scoreevent.event_id, self.event_id)
        self.assertEqual(self.scoreevent.points, self.points)
        self.assertEqual(self.scoreevent.reason, self.reason)
        self.assertEqual(self.scoreevent.competition, self.competition)
        self.assertEqual(self.scoreevent.participant, self.participant)

    def test_returns_existing_event_for_duplicate_event_id(self):
        duplicate = ScoreEventService.record_score(
            event_id=self.event_id,
            competition=self.competition,
            participant=self.participant,
            points=self.points,
            reason=self.reason,
        )

        self.assertEqual(ScoreEvent.objects.count(), 1)
        self.assertEqual(duplicate.id, self.scoreevent.id)

    def test_reject_duplicate_event_id_with_different_data(self):
        with self.assertRaises(ValidationError) as context:
            ScoreEventService.record_score(
                        event_id = self.event_id,
                        competition = self.competition,
                        participant = self.participant,
                        points = 50,
                        reason = self.reason,
                    )
            
        self.assertEqual(
            context.exception.detail["event_id"][0],
            "This event_id has already been used with different data."
        )

    def test_reject_participant_from_different_competition(self):
        other_competition = CompetitionService.create_competition(
            project=self.project,
            name="Season 2"
        )

        with self.assertRaises(ValidationError) as context:
            ScoreEventService.record_score(
                event_id = uuid.uuid4(),
                competition = other_competition,
                participant = self.participant,
                points = 50,
                reason = self.reason,
            )
                    
        self.assertEqual(
            context.exception.detail["participant"][0],
            "Participant does not belong to this competition."  
        )


 

