import secrets
from rest_framework import serializers
from .models import Company, CompanyInvitation, CompanyMembership

class CompanyMembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = CompanyMembership
        fields = ["id", "company", "user", "user_email", "role", "is_active", "created_at"]
        read_only_fields = ["created_at"]

class CompanyInvitationSerializer(serializers.ModelSerializer):
    invited_by = serializers.PrimaryKeyRelatedField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = CompanyInvitation
        fields = "__all__"

    def create(self, validated_data):
        validated_data["token"] = secrets.token_urlsafe(32)
        return super().create(validated_data)

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    memberships_count = serializers.IntegerField(source="memberships.count", read_only=True)

    class Meta:
        model = Company
        fields = "__all__"
