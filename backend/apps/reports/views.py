from rest_framework import decorators, response, status, viewsets
from apps.properties.models import Property
from .models import PropertyReport
from .serializers import PropertyReportSerializer
from .services import generate_property_report

class PropertyReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PropertyReportSerializer

    def get_queryset(self):
        return PropertyReport.objects.filter(property__company__owner=self.request.user)

    @decorators.action(detail=False, methods=["post"])
    def generate(self, request):
        property_id = request.data.get("property")
        try:
            property_obj = Property.objects.get(
                id=property_id,
                company__owner=request.user,
            )
        except Property.DoesNotExist:
            return response.Response(
                {"detail": "Immobile non trovato."},
                status=status.HTTP_404_NOT_FOUND,
            )

        report = generate_property_report(property_obj, request.user)
        return response.Response(
            PropertyReportSerializer(report, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
