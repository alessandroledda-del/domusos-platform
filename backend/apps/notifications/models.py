from django.conf import settings
from django.db import models

class Notification(models.Model):
    class Level(models.TextChoices):
        INFO = "INFO", "Informazione"
        SUCCESS = "SUCCESS", "Successo"
        WARNING = "WARNING", "Attenzione"
        ERROR = "ERROR", "Errore"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.INFO)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
