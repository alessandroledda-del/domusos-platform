from rest_framework import serializers
from .models import Finding, VerificationCertificate, VerificationRun

class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = "__all__"
        read_only_fields = [
            "verification",
            "property",
            "rule_code",
            "title",
            "description",
            "severity",
            "evidence",
            "created_at",
        ]

class VerificationRunSerializer(serializers.ModelSerializer):
    findings = FindingSerializer(many=True, read_only=True)
    property_title = serializers.CharField(source="property.title", read_only=True)

    class Meta:
        model = VerificationRun
        fields = "__all__"
        read_only_fields = [
            "requested_by",
            "status",
            "score",
            "passed_rules",
            "warning_rules",
            "failed_rules",
            "engine_version",
            "summary",
            "started_at",
            "completed_at",
        ]

class VerificationCertificateSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source="property.title", read_only=True)

    class Meta:
        model = VerificationCertificate
        fields = "__all__"
        read_only_fields = [
            "verification",
            "property",
            "issued_by",
            "public_code",
            "status",
            "verified_level",
            "score",
            "snapshot",
            "pdf_file",
            "issued_at",
            "expires_at",
            "revoked_at",
            "revocation_reason",
        ]
