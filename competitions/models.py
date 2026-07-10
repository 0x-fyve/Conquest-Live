from django.db import models
import uuid
from projects.models import Project
# Create your models here.

class CompetitionStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    LIVE = "LIVE", "Live"
    ENDED = "ENDED", "Ended"
    ARCHIVED = "ARCHIVED", "Archived"

class Competition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, related_name="competitions", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=CompetitionStatus.choices,
        default=CompetitionStatus.DRAFT,
    )
    rules = models.JSONField(default=dict, blank=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "name"],
                name="unique_competition_name_per_project",
            ),
            models.UniqueConstraint(
                fields=["project", "slug"],
                name="unique_competition_slug_per_project",
            ),
        ]

    def __str__(self):
        return f"{self.project.name} - {self.name}"
