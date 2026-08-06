from rest_framework import serializers
from .models import OnboardingProgress

class OnboardingProgressSerializer(serializers.ModelSerializer):
    completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = OnboardingProgress
        fields = "__all__"
        read_only_fields = [
            "user",
            "organization_created",
            "profile_completed",
            "first_property_created",
            "first_document_uploaded",
            "first_service_ordered",
            "first_verification_run",
            "completed",
            "updated_at",
        ]

    def get_completion_percentage(self, obj):
        fields = [
            obj.organization_created,
            obj.profile_completed,
            obj.first_property_created,
            obj.first_document_uploaded,
            obj.first_service_ordered,
            obj.first_verification_run,
        ]
        return round(sum(1 for value in fields if value) / len(fields) * 100)
