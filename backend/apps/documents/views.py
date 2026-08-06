from django.db.models import Max
from rest_framework import decorators, response, status, viewsets
from .models import Document, DocumentVersion
from .serializers import DocumentSerializer, DocumentVersionSerializer
from .tasks import process_document_task
from apps.properties.services import refresh_domus_score
from apps.properties.access import accessible_properties

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(
            property__in=accessible_properties(self.request.user)
        ).prefetch_related("versions")

    def perform_create(self, serializer):
        document = serializer.save(
            uploaded_by=self.request.user,
            status=Document.Status.QUEUED,
        )
        DocumentVersion.objects.create(
            document=document,
            version_number=1,
            file=document.file,
            uploaded_by=self.request.user,
            notes="Versione iniziale",
        )
        refresh_domus_score(document.property)
        process_document_task.delay(document.id)

    def perform_destroy(self, instance):
        property_obj = instance.property
        instance.delete()
        refresh_domus_score(property_obj)

    @decorators.action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        document = self.get_object()
        document.status = Document.Status.QUEUED
        document.processing_error = ""
        document.save(update_fields=["status", "processing_error"])
        task = process_document_task.delay(document.id)
        return response.Response(
            {"task_id": task.id, "status": "QUEUED"},
            status=status.HTTP_202_ACCEPTED,
        )

    @decorators.action(detail=True, methods=["post"])
    def add_version(self, request, pk=None):
        document = self.get_object()
        serializer = DocumentVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_max = document.versions.aggregate(value=Max("version_number"))["value"] or 0
        version = serializer.save(
            document=document,
            version_number=current_max + 1,
            uploaded_by=request.user,
        )
        document.file = version.file
        document.status = Document.Status.QUEUED
        document.processing_error = ""
        document.save(update_fields=["file", "status", "processing_error"])
        process_document_task.delay(document.id)
        return response.Response(
            DocumentVersionSerializer(version).data,
            status=status.HTTP_201_CREATED,
        )

class DocumentVersionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DocumentVersionSerializer

    def get_queryset(self):
        return DocumentVersion.objects.filter(
            document__property__in=accessible_properties(self.request.user)
        ).select_related("document")
