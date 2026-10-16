from django.db.models import Q
from rest_framework import exceptions, viewsets
from apps.properties.access import accessible_properties, editable_properties
from .models import Case, Task
from .serializers import CaseSerializer, TaskSerializer

PARTNER_CASE_FIELDS = {"status", "notes"}
PARTNER_TASK_FIELDS = {"status"}

class CaseViewSet(viewsets.ModelViewSet):
    serializer_class = CaseSerializer

    def get_queryset(self):
        return (
            Case.objects.filter(
                Q(property__in=accessible_properties(self.request.user))
                | Q(assigned_to=self.request.user)
            )
            .distinct()
            .prefetch_related("tasks")
        )

    def perform_create(self, serializer):
        property_obj = serializer.validated_data["property"]
        if not editable_properties(self.request.user).filter(pk=property_obj.pk).exists():
            raise exceptions.PermissionDenied("Non puoi creare pratiche per questo immobile.")
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        case = serializer.instance
        if editable_properties(self.request.user).filter(pk=case.property_id).exists():
            serializer.save()
            return
        if case.assigned_to_id != self.request.user.id:
            raise exceptions.PermissionDenied("Non puoi modificare questa pratica.")
        disallowed = set(serializer.validated_data) - PARTNER_CASE_FIELDS
        if disallowed:
            raise exceptions.PermissionDenied("Il partner può aggiornare solo stato e note.")
        serializer.save()

    def perform_destroy(self, instance):
        if not editable_properties(self.request.user).filter(pk=instance.property_id).exists():
            raise exceptions.PermissionDenied("Non puoi eliminare questa pratica.")
        instance.delete()

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            Q(case__property__in=accessible_properties(self.request.user))
            | Q(assignee=self.request.user)
            | Q(case__assigned_to=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        case = serializer.validated_data["case"]
        if not editable_properties(self.request.user).filter(pk=case.property_id).exists():
            raise exceptions.PermissionDenied("Non puoi creare attività per questa pratica.")
        serializer.save()

    def perform_update(self, serializer):
        task = serializer.instance
        if editable_properties(self.request.user).filter(pk=task.case.property_id).exists():
            serializer.save()
            return
        if task.assignee_id != self.request.user.id and task.case.assigned_to_id != self.request.user.id:
            raise exceptions.PermissionDenied("Non puoi modificare questa attività.")
        disallowed = set(serializer.validated_data) - PARTNER_TASK_FIELDS
        if disallowed:
            raise exceptions.PermissionDenied("Il partner può aggiornare solo lo stato dell'attività.")
        serializer.save()

    def perform_destroy(self, instance):
        if not editable_properties(self.request.user).filter(pk=instance.case.property_id).exists():
            raise exceptions.PermissionDenied("Non puoi eliminare questa attività.")
        instance.delete()
