from django.conf import settings
from django.db import models
from apps.properties.models import Property

class Document(models.Model):
    class Type(models.TextChoices):
        DEED = "DEED", "Atto di provenienza"
        CADASTRAL = "CADASTRAL", "Visura catastale"
        PLAN = "PLAN", "Planimetria catastale"
        MAP = "MAP", "Estratto di mappa"
        ENERGY = "ENERGY", "APE"
        BUILDING = "BUILDING", "Titolo edilizio"
        MORTGAGE = "MORTGAGE", "Visura ipotecaria"
        OTHER = "OTHER", "Altro"

    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "Caricato"
        QUEUED = "QUEUED", "In coda"
        PROCESSING = "PROCESSING", "In elaborazione"
        VERIFIED = "VERIFIED", "Verificato"
        WARNING = "WARNING", "Criticità"
        FAILED = "FAILED", "Elaborazione fallita"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=30, choices=Type.choices)
    file = models.FileField(upload_to="property_documents/%Y/%m/")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED)
    notes = models.TextField(blank=True)
    extracted_data = models.JSONField(default=dict, blank=True)
    processing_confidence = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    processing_error = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def latest_version(self):
        return self.versions.order_by("-version_number").first()

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    file = models.FileField(upload_to="document_versions/%Y/%m/")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("document", "version_number")
        ordering = ["-version_number"]

    def __str__(self):
        return f"{self.document.name} v{self.version_number}"
