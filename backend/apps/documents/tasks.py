from celery import shared_task
from django.utils import timezone
from .antivirus import scan_file
from .models import Document
from .services import process_document
from apps.integrations.tasks import publish_event
from apps.notifications.tasks import send_email_task

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_document_task(self, document_id):
    document = Document.objects.select_related("uploaded_by").get(id=document_id)
    document.status = Document.Status.PROCESSING
    document.processing_error = ""
    document.save(update_fields=["status", "processing_error"])

    try:
        with document.file.open("rb") as file_obj:
            antivirus_result = scan_file(file_obj)

        metadata = process_document(document)
        metadata["antivirus"] = antivirus_result
        document.extracted_data = metadata
        document.processed_at = timezone.now()
        document.status = Document.Status.VERIFIED
        document.save(update_fields=["extracted_data", "processed_at", "status"])

        send_email_task.delay(
            document.uploaded_by.email,
            f"Documento elaborato: {document.name}",
            "document_processed",
            {
                "document_name": document.name,
                "status": document.status,
                "confidence": str(document.processing_confidence or ""),
            },
        )

        publish_event(
            "document.processed",
            {
                "document_id": document.id,
                "property_id": document.property_id,
                "status": document.status,
                "document_type": document.document_type,
            },
        )
        return metadata
    except Exception as exc:
        document.status = Document.Status.FAILED
        document.processing_error = str(exc)[:1000]
        document.save(update_fields=["status", "processing_error"])
        raise
