from django.db import transaction
from django.db.models import Max
from rest_framework import decorators, exceptions, response, status, viewsets
from apps.properties.access import accessible_properties, editable_properties
from apps.properties.services import refresh_domus_score
from .models import Document, DocumentVersion
from .serializers import DocumentSerializer, DocumentVersionSerializer
from .tasks import process_document_task

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(
            property__in=accessible_properties(self.request.user)
        ).prefetch_related("versions")

    def _ensure_write_access(self, document):
        if not editable_properties(self.request.user).filter(pk=document.property_id).exists():
            raise exceptions.PermissionDenied("Non puoi modificare documenti per questo immobile.")

    def perform_create(self, serializer):
        property_obj = serializer.validated_data["property"]
        if not editable_properties(self.request.user).filter(pk=property_obj.pk).exists():
            raise exceptions.PermissionDenied("Non puoi caricare documenti per questo immobile.")
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

    def perform_update(self, serializer):
        self._ensure_write_access(serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_write_access(instance)
        property_obj = instance.property
        instance.delete()
        refresh_domus_score(property_obj)

    @decorators.action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        document = self.get_object()
        self._ensure_write_access(document)
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
        self._ensure_write_access(document)
        serializer = DocumentVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            locked = Document.objects.select_for_update().get(pk=document.pk)
            current_max = locked.versions.aggregate(value=Max("version_number"))["value"] or 0
            version = serializer.save(
                document=locked,
                version_number=current_max + 1,
                uploaded_by=request.user,
            )
            locked.file = version.file
            locked.status = Document.Status.QUEUED
            locked.processing_error = ""
            locked.save(update_fields=["file", "status", "processing_error"])
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
