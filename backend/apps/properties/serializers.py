from rest_framework import serializers
from apps.companies.access import accessible_companies
from .models import Owner, Property

class OwnerSerializer(serializers.ModelSerializer):
    linked_user_email = serializers.EmailField(source="linked_user.email", read_only=True)

    class Meta:
        model = Owner
        fields = "__all__"

    def validate_property(self, value):
        request = self.context.get("request")
        if request and not Property.objects.filter(
            id=value.id,
            company__in=accessible_companies(request.user),
        ).exists():
            raise serializers.ValidationError("Immobile non accessibile.")
        return value

class PropertySerializer(serializers.ModelSerializer):
    owners = OwnerSerializer(many=True, read_only=True)
    documents_count = serializers.IntegerField(source="documents.count", read_only=True)
    cases_count = serializers.IntegerField(source="cases.count", read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = "__all__"

    def validate_company(self, value):
        request = self.context.get("request")
        if request and not accessible_companies(request.user).filter(id=value.id).exists():
            raise serializers.ValidationError("Organizzazione non accessibile.")
        return value
