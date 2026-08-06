import secrets
from django.conf import settings
from django.db import models
from apps.properties.models import Property

class VerificationRun(models.Model):
    class Status(models.TextChoices):
        RUNNING = "RUNNING", "In esecuzione"
        COMPLETED = "COMPLETED", "Completata"
        FAILED = "FAILED", "Fallita"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="verification_runs")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RUNNING)
    score = models.PositiveSmallIntegerField(default=0)
    passed_rules = models.PositiveIntegerField(default=0)
    warning_rules = models.PositiveIntegerField(default=0)
    failed_rules = models.PositiveIntegerField(default=0)
    engine_version = models.CharField(max_length=30, default="0.8")
    summary = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

class Finding(models.Model):
    class Severity(models.TextChoices):
        INFO = "INFO", "Informazione"
        LOW = "LOW", "Bassa"
        MEDIUM = "MEDIUM", "Media"
        HIGH = "HIGH", "Alta"
        CRITICAL = "CRITICAL", "Critica"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Aperta"
        ACKNOWLEDGED = "ACKNOWLEDGED", "Presa in carico"
        RESOLVED = "RESOLVED", "Risolta"
        ACCEPTED_RISK = "ACCEPTED_RISK", "Rischio accettato"

    verification = models.ForeignKey(VerificationRun, on_delete=models.CASCADE, related_name="findings")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="compliance_findings")
    rule_code = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=Severity.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    evidence = models.JSONField(default=dict, blank=True)
    resolution_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_compliance_findings",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["severity", "created_at"]

class VerificationCertificate(models.Model):
    class Status(models.TextChoices):
        VALID = "VALID", "Valido"
        REVOKED = "REVOKED", "Revocato"
        EXPIRED = "EXPIRED", "Scaduto"

    verification = models.OneToOneField(
        VerificationRun,
        on_delete=models.PROTECT,
        related_name="certificate",
    )
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="verification_certificates")
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    public_code = models.CharField(max_length=40, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.VALID)
    verified_level = models.CharField(max_length=30)
    score = models.PositiveSmallIntegerField()
    snapshot = models.JSONField(default=dict)
    pdf_file = models.FileField(upload_to="verification_certificates/%Y/%m/", blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    revocation_reason = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.public_code:
            self.public_code = f"DV-{secrets.token_hex(10).upper()}"
        super().save(*args, **kwargs)
