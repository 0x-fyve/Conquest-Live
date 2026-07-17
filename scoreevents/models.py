from django.db import models
from participants.models import Participant
from competitions.models import Competition
import uuid
# Create your models here.
class ScoreEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(unique=True, default=uuid.uuid4)
    competition = models.ForeignKey(Competition, related_name='scoreevents', on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, related_name='scoreevents', on_delete=models.CASCADE)
    points = models.IntegerField()
    reason = models.CharField(max_length=255,blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.participant.display_name}  {self.points}"


