from rest_framework import response, views
from .models import Property
from .serializers import PropertySerializer

class CustomerPortalView(views.APIView):
    def get(self, request):
        properties = (
            Property.objects.filter(owners__linked_user=request.user)
            .distinct()
            .prefetch_related("owners", "documents", "cases")
        )
        return response.Response({
            "properties": PropertySerializer(properties, many=True).data,
            "documents_total": sum(item.documents.count() for item in properties),
            "open_cases": sum(
                item.cases.exclude(status__in=["COMPLETED", "CANCELLED"]).count()
                for item in properties
            ),
        })
