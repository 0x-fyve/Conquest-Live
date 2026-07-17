from django.db import models
from competitions.models import Competition
import uuid
# Create your models here.

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(Competition, related_name='participants', on_delete=models.CASCADE)
    external_id = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["joined_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "external_id"],
                name="unique_participant_per_competition",
            )
        ]

    def __str__(self):
        return f"{self.competition.name} - {self.display_name}"  

