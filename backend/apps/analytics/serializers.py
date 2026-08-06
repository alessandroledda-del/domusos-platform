from rest_framework import serializers
from .models import AnalyticsSnapshot

class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsSnapshot
        fields = "__all__"
        read_only_fields = [
            "scope",
            "scope_id",
            "period_date",
            "metrics",
            "generated_by",
            "created_at",
        ]
