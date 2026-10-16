from rest_framework import serializers
from apps.companies.access import editable_companies
from .access import editable_properties
from .models import Owner, Property

class OwnerSerializer(serializers.ModelSerializer):
    linked_user_email = serializers.EmailField(source="linked_user.email", read_only=True)

    class Meta:
        model = Owner
        fields = "__all__"

    def validate_property(self, value):
        request = self.context.get("request")
        if request and not editable_properties(request.user).filter(id=value.id).exists():
            raise serializers.ValidationError("Non puoi modificare i proprietari di questo immobile.")
        return value

class PropertySerializer(serializers.ModelSerializer):
    owners = OwnerSerializer(many=True, read_only=True)
    documents_count = serializers.IntegerField(source="documents.count", read_only=True)
    cases_count = serializers.IntegerField(source="cases.count", read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ["created_by", "domus_score", "status", "created_at", "updated_at"]

    def validate_company(self, value):
        request = self.context.get("request")
        if request and not editable_companies(request.user).filter(id=value.id).exists():
            raise serializers.ValidationError("Non puoi modificare immobili per questa organizzazione.")
        return value
