from django.conf import settings
from django.db import models
from apps.properties.models import Property

class Case(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Aperta"
        IN_PROGRESS = "IN_PROGRESS", "In lavorazione"
        WAITING = "WAITING", "In attesa"
        COMPLETED = "COMPLETED", "Completata"
        CANCELLED = "CANCELLED", "Annullata"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="cases")
    title = models.CharField(max_length=255)
    service_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_cases",
    )
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_cases")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "Da fare"
        DOING = "DOING", "In corso"
        DONE = "DONE", "Completata"

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TODO)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
