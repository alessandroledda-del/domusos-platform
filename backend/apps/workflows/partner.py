from rest_framework import response, views
from .models import Case
from .serializers import CaseSerializer

class PartnerPortalView(views.APIView):
    def get(self, request):
        cases = (
            Case.objects.filter(assigned_to=request.user)
            .select_related("property")
            .prefetch_related("tasks")
        )
        return response.Response({
            "assigned_cases": CaseSerializer(cases, many=True).data,
            "open_cases": cases.exclude(status__in=["COMPLETED", "CANCELLED"]).count(),
            "overdue_tasks": sum(
                case.tasks.filter(status__in=["TODO", "DOING"], due_date__lt=__import__("datetime").date.today()).count()
                for case in cases
            ),
        })
