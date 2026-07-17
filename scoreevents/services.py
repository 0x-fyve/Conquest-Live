from .models import ScoreEvent
from rest_framework.exceptions import ValidationError

class ScoreEventService():
    @staticmethod
    def record_score(
        event_id,
        competition,
        participant,
        points,
        reason="",
        metadata=None
    ):
        
        if participant.competition != competition:
            raise ValidationError(
                {"participant": ["Participant does not belong to this competition."]}
            )
        
        if metadata is None:
                metadata = {}
        
        existing = ScoreEvent.objects.filter(event_id=event_id).first()

        if existing:
            if (
                existing.participant != participant or
                existing.competition != competition or
                existing.points != points or
                existing.reason != reason or
                existing.metadata != metadata
            ):
                raise ValidationError({
                    "event_id": [
                        "This event_id has already been used with different data."
                    ]
                })

            return existing
        
        
        score_event = ScoreEvent.objects.create(
            event_id=event_id,
            competition=competition,
            participant=participant,
            points=points,
            reason=reason,
            metadata=metadata
        )
        return score_event

  
