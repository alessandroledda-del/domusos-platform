from apps.notifications.models import Notification
from .ocr import extract_metadata

def process_document(document):
    metadata = extract_metadata(document)
    document.extracted_data = metadata
    document.processing_confidence = metadata["confidence"]

    if document.document_type == "OTHER":
        document.document_type = metadata["suggested_document_type"]

    document.save(
        update_fields=[
            "extracted_data",
            "processing_confidence",
            "document_type",
        ]
    )

    Notification.objects.create(
        user=document.uploaded_by,
        title="Documento elaborato",
        message=f"Il documento '{document.name}' è stato analizzato.",
        level=Notification.Level.SUCCESS,
    )
    return metadata
