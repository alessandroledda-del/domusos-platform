from decimal import Decimal
from django.db.models import Q
from django.utils import timezone
from rest_framework import decorators, permissions, response, status, viewsets
from apps.orders.models import Order
from apps.workflows.models import Case
from .models import Commission, PartnerAssignment, PartnerProfile, PartnerService, Payout
from .serializers import (
    CommissionSerializer,
    PartnerAssignmentSerializer,
    PartnerProfileSerializer,
    PartnerServiceSerializer,
    PayoutSerializer,
)
from .services import assign_partner, complete_assignment, create_payout, rank_partners

class PartnerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerProfileSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = PartnerProfile.objects.all()
        else:
            queryset = PartnerProfile.objects.filter(
                Q(status=PartnerProfile.Status.ACTIVE) |
                Q(user=self.request.user)
            )
        queryset = queryset.prefetch_related("service_offers__service")
        province = self.request.query_params.get("province")
        professional_type = self.request.query_params.get("professional_type")
        if province:
            queryset = queryset.filter(provinces__contains=[province.upper()])
        if professional_type:
            queryset = queryset.filter(professional_type__icontains=professional_type)
        return queryset.distinct()

    def perform_create(self, serializer):
        if hasattr(self.request.user, "partner_profile"):
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Esiste già un profilo partner.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_staff and serializer.instance.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Non puoi modificare questo profilo.")
        serializer.save()

    @decorators.action(detail=False, methods=["get"])
    def ranked(self, request):
        profiles = rank_partners(
            self.get_queryset().filter(status=PartnerProfile.Status.ACTIVE)
        )
        return response.Response(
            PartnerProfileSerializer(profiles, many=True).data
        )

class PartnerServiceViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerServiceSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return PartnerService.objects.all()
        return PartnerService.objects.filter(partner__user=self.request.user)

class PartnerAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerAssignmentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return PartnerAssignment.objects.all().select_related("partner", "case")
        return PartnerAssignment.objects.filter(
            partner__user=self.request.user
        ).select_related("partner", "case")

    @decorators.action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser],
    )
    def assign(self, request):
        try:
            case = Case.objects.get(id=request.data.get("case"))
            partner = PartnerProfile.objects.get(
                id=request.data.get("partner"),
                status=PartnerProfile.Status.ACTIVE,
            )
            order = None
            if request.data.get("order"):
                order = Order.objects.get(id=request.data.get("order"))
            assignment = assign_partner(
                case=case,
                partner=partner,
                amount=Decimal(str(request.data.get("amount"))),
                user=request.user,
                order=order,
                due_at=request.data.get("due_at"),
                notes=request.data.get("notes", ""),
            )
        except Exception as exc:
            return response.Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response.Response(
            PartnerAssignmentSerializer(assignment).data,
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        assignment = self.get_object()
        if assignment.status != PartnerAssignment.Status.PROPOSED:
            return response.Response(
                {"detail": "Assegnazione non accettabile nello stato corrente."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        assignment.status = PartnerAssignment.Status.ACCEPTED
        assignment.accepted_at = timezone.now()
        assignment.save(update_fields=["status", "accepted_at"])
        return response.Response(PartnerAssignmentSerializer(assignment).data)

    @decorators.action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        assignment = self.get_object()
        if assignment.status not in {
            PartnerAssignment.Status.ACCEPTED,
            PartnerAssignment.Status.IN_PROGRESS,
        }:
            return response.Response(
                {"detail": "Assegnazione non completabile nello stato corrente."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        complete_assignment(assignment)
        return response.Response(PartnerAssignmentSerializer(assignment).data)

class CommissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommissionSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Commission.objects.all()
        return Commission.objects.filter(
            assignment__partner__user=self.request.user
        )

class PayoutViewSet(viewsets.ModelViewSet):
    serializer_class = PayoutSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payout.objects.all()
        return Payout.objects.filter(partner__user=self.request.user)

    @decorators.action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser],
    )
    def generate(self, request):
        try:
            partner = PartnerProfile.objects.get(id=request.data.get("partner"))
            payout, commissions = create_payout(
                partner,
                request.data.get("period_start"),
                request.data.get("period_end"),
            )
        except Exception as exc:
            return response.Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response.Response(
            {
                "payout": PayoutSerializer(payout).data,
                "commission_ids": list(commissions.values_list("id", flat=True)),
            },
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser],
    )
    def approve(self, request, pk=None):
        payout = self.get_object()
        payout.status = Payout.Status.APPROVED
        payout.approved_by = request.user
        payout.approved_at = timezone.now()
        payout.save(update_fields=["status", "approved_by", "approved_at"])
        return response.Response(PayoutSerializer(payout).data)

class MarketplaceDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        assignments = PartnerAssignment.objects.all()
        commissions = Commission.objects.all()
        payouts = Payout.objects.all()
        return response.Response({
            "partners_active": PartnerProfile.objects.filter(
                status=PartnerProfile.Status.ACTIVE
            ).count(),
            "assignments_open": assignments.exclude(
                status__in=[
                    PartnerAssignment.Status.COMPLETED,
                    PartnerAssignment.Status.CANCELLED,
                ]
            ).count(),
            "assignments_completed": assignments.filter(
                status=PartnerAssignment.Status.COMPLETED
            ).count(),
            "commissions_earned": str(sum(
                (
                    item.platform_amount
                    for item in commissions.filter(status=Commission.Status.EARNED)
                ),
                Decimal("0.00"),
            )),
            "partner_payable": str(sum(
                (
                    item.partner_amount
                    for item in commissions.filter(status=Commission.Status.EARNED)
                ),
                Decimal("0.00"),
            )),
            "payouts_pending": payouts.filter(
                status__in=[Payout.Status.DRAFT, Payout.Status.APPROVED]
            ).count(),
        })
