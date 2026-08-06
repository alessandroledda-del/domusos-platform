from rest_framework import serializers
from .models import PropertyReport

class PropertyReportSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PropertyReport
        fields = "__all__"
        read_only_fields = ["snapshot", "file", "created_at"]
