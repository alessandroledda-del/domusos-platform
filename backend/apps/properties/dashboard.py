from rest_framework import response, views
from .views import accessible_properties
from apps.documents.models import Document
from apps.workflows.models import Case

class DashboardView(views.APIView):
    def get(self, request):
        properties = accessible_properties(request.user)
        documents = Document.objects.filter(property__in=properties)
        cases = Case.objects.filter(property__in=properties)

        return response.Response({
            "properties_total": properties.count(),
            "properties_verified": properties.filter(status="VERIFIED").count(),
            "documents_total": documents.count(),
            "cases_open": cases.exclude(status__in=["COMPLETED", "CANCELLED"]).count(),
            "average_domus_score": round(
                sum(properties.values_list("domus_score", flat=True)) / properties.count(),
                2,
            ) if properties.exists() else 0,
        })
