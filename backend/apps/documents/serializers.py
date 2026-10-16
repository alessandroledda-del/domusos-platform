from rest_framework import serializers
from apps.properties.access import editable_properties
from .models import Document, DocumentVersion

class DocumentVersionSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DocumentVersion
        fields = "__all__"
        read_only_fields = ["document", "version_number", "uploaded_by", "uploaded_at"]

    def validate_file(self, value):
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError("Dimensione massima: 20 MB.")
        return value

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)
    versions = DocumentVersionSerializer(many=True, read_only=True)
    latest_version_number = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = [
            "uploaded_by",
            "status",
            "extracted_data",
            "processing_confidence",
            "processing_error",
            "processed_at",
            "uploaded_at",
        ]

    def get_latest_version_number(self, obj):
        latest = obj.latest_version
        return latest.version_number if latest else None

    def validate_property(self, value):
        request = self.context.get("request")
        if request and not editable_properties(request.user).filter(id=value.id).exists():
            raise serializers.ValidationError("Non puoi modificare documenti per questo immobile.")
        return value

    def validate_file(self, value):
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError("Dimensione massima: 20 MB.")
        allowed = {"application/pdf", "image/jpeg", "image/png", "image/tiff"}
        content_type = getattr(value, "content_type", None)
        if content_type and content_type not in allowed:
            raise serializers.ValidationError("Formato non supportato.")
        return value
