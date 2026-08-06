from rest_framework import decorators, response, viewsets
from .access import accessible_properties
from .models import Owner, Property
from .serializers import OwnerSerializer, PropertySerializer
from .services import refresh_domus_score

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer

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
        score = refresh_domus_score(property_obj)
        return response.Response({"domus_score": score})

class OwnerViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer

    def get_queryset(self):
        return Owner.objects.filter(
            property__in=accessible_properties(self.request.user)
        )

    def perform_create(self, serializer):
        owner = serializer.save()
        refresh_domus_score(owner.property)
