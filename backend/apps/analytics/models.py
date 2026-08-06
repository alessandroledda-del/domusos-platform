from django.conf import settings
from django.db import models

class AnalyticsSnapshot(models.Model):
    scope = models.CharField(max_length=50, default="GLOBAL")
    scope_id = models.CharField(max_length=100, blank=True)
    period_date = models.DateField()
    metrics = models.JSONField(default=dict)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("scope", "scope_id", "period_date")
        ordering = ["-period_date", "-created_at"]

    def __str__(self):
        return f"{self.scope}:{self.scope_id or 'global'} {self.period_date}"
