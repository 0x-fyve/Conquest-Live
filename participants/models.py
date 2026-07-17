from django.db import models
from competitions.models import Competition
import uuid
# Create your models here.

class Participant(models.Model):
    id = models.UUIDField()
