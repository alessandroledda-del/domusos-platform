from rest_framework import decorators, response, viewsets
from .access import accessible_properties
from .models import Owner, Property
from .permissions import OwnerWritePermission, PropertyWritePermission
from .serializers import OwnerSerializer, PropertySerializer
from .services import refresh_domus_score

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [PropertyWritePermission]

    def get_queryset(self):
        return (
            accessible_properties(self.request.user)
            .select_related("company")
            .prefetch_related("owners", "documents", "cases")
        )

    def perform_create(self, serializer):
        property_obj = serializer.save(created_by=self.request.user)
        refresh_domus_score(property_obj)

    @decorators.action(detail=True, methods=["post"])
    def refresh_score(self, request, pk=None):
        property_obj = self.get_object()
        self.check_object_permissions(request, property_obj)
        score = refresh_domus_score(property_obj)
        return response.Response({"domus_score": score})

class OwnerViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    permission_classes = [OwnerWritePermission]

    def get_queryset(self):
        return Owner.objects.filter(
            property__in=accessible_properties(self.request.user)
        ).select_related("property", "linked_user")

    def perform_create(self, serializer):
        owner = serializer.save()
        refresh_domus_score(owner.property)

    def perform_update(self, serializer):
        property_obj = serializer.instance.property
        owner = serializer.save()
        refresh_domus_score(property_obj)
        if owner.property_id != property_obj.id:
            refresh_domus_score(owner.property)

    def perform_destroy(self, instance):
        property_obj = instance.property
        instance.delete()
        refresh_domus_score(property_obj)
