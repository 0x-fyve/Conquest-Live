from django.db import models
from projects.models import Project
import uuid
from django.conf import settings

# Create your models here.
class APIKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    name = models.CharField(max_length=100)

    prefix = models.CharField(max_length=20)

    hashed_key = models.CharField(
        max_length=64,
        unique=True,
    )

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "name"],
                name="unique_api_key_name_per_project",
            )
        ]
        indexes = [
            models.Index(fields=["project", "is_active"]),
        ]