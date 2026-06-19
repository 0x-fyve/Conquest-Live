from django.db import models
import secrets

# Create your models here.import secrets
class App(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=64, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_hex(32)
        super().save(*args, **kwargs)   
        