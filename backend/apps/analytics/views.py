import csv
from django.http import HttpResponse
from rest_framework import decorators, permissions, response, viewsets
from .models import AnalyticsSnapshot
from .serializers import AnalyticsSnapshotSerializer
from .services import build_global_metrics, create_global_snapshot

class AnalyticsDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        return response.Response(build_global_metrics())

    @decorators.action(detail=False, methods=["post"])
    def snapshot(self, request):
        snapshot = create_global_snapshot(request.user)
        return response.Response(AnalyticsSnapshotSerializer(snapshot).data)

    @decorators.action(detail=False, methods=["get"])
    def export_csv(self, request):
        metrics = build_global_metrics()
        http_response = HttpResponse(content_type="text/csv")
        http_response["Content-Disposition"] = 'attachment; filename="domusos-kpi.csv"'

        writer = csv.writer(http_response)
        writer.writerow(["section", "metric", "value"])
        for section, values in metrics.items():
            for key, value in values.items():
                writer.writerow([section, key, value])

        return http_response

class AnalyticsSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnalyticsSnapshotSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = AnalyticsSnapshot.objects.all()
