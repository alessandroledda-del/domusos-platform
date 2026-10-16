import secrets
from rest_framework import serializers
from .access import user_can_admin_company
from .models import Company, CompanyInvitation, CompanyMembership

class CompanyMembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = CompanyMembership
        fields = ["id", "company", "user", "user_email", "role", "is_active", "created_at"]
        read_only_fields = ["created_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        company = attrs.get("company") or getattr(self.instance, "company", None)
        if request and company and not user_can_admin_company(request.user, company):
            raise serializers.ValidationError("Non puoi amministrare i membri di questa azienda.")
        if self.instance:
            if "company" in attrs and attrs["company"].pk != self.instance.company_id:
                raise serializers.ValidationError({"company": "Il collegamento aziendale non è modificabile."})
            if "user" in attrs and attrs["user"].pk != self.instance.user_id:
                raise serializers.ValidationError({"user": "L'utente della membership non è modificabile."})
        return attrs

class CompanyInvitationSerializer(serializers.ModelSerializer):
    invited_by = serializers.PrimaryKeyRelatedField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = CompanyInvitation
        fields = "__all__"
        read_only_fields = ["invited_by", "token", "created_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        company = attrs.get("company") or getattr(self.instance, "company", None)
        if request and company and not user_can_admin_company(request.user, company):
            raise serializers.ValidationError("Non puoi gestire gli inviti di questa azienda.")
        if self.instance and "company" in attrs and attrs["company"].pk != self.instance.company_id:
            raise serializers.ValidationError({"company": "L'azienda dell'invito non è modificabile."})
        return attrs

    def create(self, validated_data):
        validated_data["token"] = secrets.token_urlsafe(32)
        return super().create(validated_data)

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    memberships_count = serializers.IntegerField(source="memberships.count", read_only=True)

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["owner", "created_at"]
