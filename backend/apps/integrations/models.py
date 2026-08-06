from django.conf import settings
from django.db import models

class WebhookEndpoint(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="webhook_endpoints")
    name = models.CharField(max_length=120)
    url = models.URLField()
    secret = models.CharField(max_length=255, blank=True)
    subscribed_events = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class WebhookDelivery(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "In attesa"
        DELIVERED = "DELIVERED", "Consegnato"
        FAILED = "FAILED", "Fallito"

    endpoint = models.ForeignKey(WebhookEndpoint, on_delete=models.CASCADE, related_name="deliveries")
    event_type = models.CharField(max_length=100)
    event_id = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    attempts = models.PositiveIntegerField(default=0)
    response_status = models.PositiveIntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("endpoint", "event_id")
        ordering = ["-created_at"]

class InboundEvent(models.Model):
    provider = models.CharField(max_length=50)
    event_id = models.CharField(max_length=150)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("provider", "event_id")
