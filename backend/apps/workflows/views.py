from django.db.models import Q
from rest_framework import viewsets
from apps.properties.access import accessible_properties
from .models import Case, Task
from .serializers import CaseSerializer, TaskSerializer

class CaseViewSet(viewsets.ModelViewSet):
    serializer_class = CaseSerializer

    def get_queryset(self):
        return (
            Case.objects.filter(
                Q(property__in=accessible_properties(self.request.user)) |
                Q(assigned_to=self.request.user)
            )
            .distinct()
            .prefetch_related("tasks")
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            Q(case__property__in=accessible_properties(self.request.user)) |
            Q(assignee=self.request.user)
        ).distinct()
