from django.db import models
from accounts.models import App
# Create your models here.
class Participant(models.Model):
    app  = models.ForeignKey(App, on_delete=models.CASCADE, related_name="participants")
    external_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ["app", "external_id"]

    def __str__(self):
        return self.username
        