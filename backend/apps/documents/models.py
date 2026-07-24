from django.db import models
from apps.properties.models import Property

class Document(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50)
    file = models.FileField(upload_to="property_documents/")
    status = models.CharField(
        max_length=20,
        default="UPLOADED"
    )

    def __str__(self):
        return self.name
