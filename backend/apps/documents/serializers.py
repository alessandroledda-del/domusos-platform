from rest_framework import serializers
from .models import Document, DocumentVersion

class DocumentVersionSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DocumentVersion
        fields = "__all__"
        read_only_fields = ["version_number", "uploaded_at"]

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

    def get_latest_version_number(self, obj):
        latest = obj.latest_version
        return latest.version_number if latest else None

    def validate_file(self, value):
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError("Dimensione massima: 20 MB.")
        allowed = {"application/pdf", "image/jpeg", "image/png"}
        content_type = getattr(value, "content_type", None)
        if content_type and content_type not in allowed:
            raise serializers.ValidationError("Formato non supportato.")
        return value
