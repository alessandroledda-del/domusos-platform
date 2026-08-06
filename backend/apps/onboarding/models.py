from django.conf import settings
from django.db import models

class OnboardingProgress(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="onboarding_progress",
    )
    organization_created = models.BooleanField(default=False)
    profile_completed = models.BooleanField(default=False)
    first_property_created = models.BooleanField(default=False)
    first_document_uploaded = models.BooleanField(default=False)
    first_service_ordered = models.BooleanField(default=False)
    first_verification_run = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    dismissed = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def refresh_completion(self):
        required = [
            self.organization_created,
            self.profile_completed,
            self.first_property_created,
            self.first_document_uploaded,
        ]
        self.completed = all(required)
        self.save(update_fields=["completed", "updated_at"])
        return self.completed
