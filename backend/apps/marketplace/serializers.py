from rest_framework import serializers
from .models import Commission, PartnerAssignment, PartnerProfile, PartnerService, Payout
from .services import partner_rank_score

class PartnerServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = PartnerService
        fields = "__all__"

class PartnerProfileSerializer(serializers.ModelSerializer):
    service_offers = PartnerServiceSerializer(many=True, read_only=True)
    rank_score = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = PartnerProfile
        fields = "__all__"
        read_only_fields = [
            "rating",
            "completed_assignments",
            "average_completion_hours",
            "sla_compliance_rate",
            "created_at",
            "updated_at",
        ]

    def get_rank_score(self, obj):
        return partner_rank_score(obj)

class PartnerAssignmentSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source="partner.display_name", read_only=True)
    case_title = serializers.CharField(source="case.title", read_only=True)
    commission_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    partner_net_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = PartnerAssignment
        fields = "__all__"
        read_only_fields = [
            "assigned_by",
            "accepted_at",
            "completed_at",
            "created_at",
        ]

class CommissionSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source="assignment.partner.display_name", read_only=True)

    class Meta:
        model = Commission
        fields = "__all__"
        read_only_fields = fields

class PayoutSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source="partner.display_name", read_only=True)

    class Meta:
        model = Payout
        fields = "__all__"
        read_only_fields = [
            "number",
            "amount",
            "status",
            "approved_by",
            "approved_at",
            "paid_at",
            "created_at",
        ]
