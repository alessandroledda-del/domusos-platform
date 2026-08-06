from django.db.models import Q
from rest_framework import response, views
from apps.documents.models import Document
from apps.properties.views import accessible_properties
from apps.workflows.models import Case

class GlobalSearchView(views.APIView):
    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if len(query) < 2:
            return response.Response({
                "query": query,
                "properties": [],
                "documents": [],
                "cases": [],
            })

        properties_scope = accessible_properties(request.user)

        properties = properties_scope.filter(
            Q(title__icontains=query) |
            Q(address__icontains=query) |
            Q(municipality__icontains=query) |
            Q(cadastral_sheet__icontains=query) |
            Q(cadastral_particle__icontains=query) |
            Q(cadastral_subaltern__icontains=query)
        )[:20]

        documents = Document.objects.filter(
            property__in=properties_scope
        ).filter(
            Q(name__icontains=query) |
            Q(notes__icontains=query) |
            Q(document_type__icontains=query)
        )[:20]

        cases = Case.objects.filter(
            property__in=properties_scope
        ).filter(
            Q(title__icontains=query) |
            Q(service_type__icontains=query) |
            Q(notes__icontains=query)
        )[:20]

        return response.Response({
            "query": query,
            "properties": [
                {
                    "id": item.id,
                    "title": item.title,
                    "address": item.address,
                    "municipality": item.municipality,
                    "domus_score": item.domus_score,
                }
                for item in properties
            ],
            "documents": [
                {
                    "id": item.id,
                    "name": item.name,
                    "document_type": item.document_type,
                    "property_id": item.property_id,
                }
                for item in documents
            ],
            "cases": [
                {
                    "id": item.id,
                    "title": item.title,
                    "status": item.status,
                    "property_id": item.property_id,
                }
                for item in cases
            ],
        })
