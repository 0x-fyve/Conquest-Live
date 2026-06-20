from django.db import models
from accounts.models import App
# Create your models here.
class Competition(models.Model):
    RESET_CHOICES = [
        ("none", "None"),
        ("weekly", "Weekly"),
        ("monthly", 'Monthly')
    ]

    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='competitions')
    name = models.CharField(max_length=255)

    scoring_rules = models.JSONField(default=dict, blank=True)
    reset_type= models.CharField(max_length=20, choices=RESET_CHOICES, default="none")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    