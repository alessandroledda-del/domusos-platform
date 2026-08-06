from django.conf import settings
from django.db import models
from apps.properties.models import Property

class PropertyReport(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reports")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="property_reports/%Y/%m/", blank=True)
    snapshot = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
