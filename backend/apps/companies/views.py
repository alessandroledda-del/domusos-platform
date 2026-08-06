from rest_framework import exceptions, viewsets
from .access import accessible_companies, user_can_manage_company
from .models import Company, CompanyInvitation, CompanyMembership
from .serializers import (
    CompanyInvitationSerializer,
    CompanyMembershipSerializer,
    CompanySerializer,
)

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return accessible_companies(self.request.user).prefetch_related("memberships")

    def perform_create(self, serializer):
        company = serializer.save(owner=self.request.user)
        CompanyMembership.objects.get_or_create(
            company=company,
            user=self.request.user,
            defaults={"role": CompanyMembership.Role.ADMIN},
        )

class CompanyMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyMembershipSerializer

    def get_queryset(self):
        return CompanyMembership.objects.filter(
            company__in=accessible_companies(self.request.user)
        ).select_related("company", "user")

    def perform_create(self, serializer):
        company = serializer.validated_data["company"]
        if not user_can_manage_company(self.request.user, company):
            raise exceptions.PermissionDenied("Non puoi gestire i membri di questa azienda.")
        serializer.save()

class CompanyInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyInvitationSerializer

    def get_queryset(self):
        return CompanyInvitation.objects.filter(
            company__in=accessible_companies(self.request.user)
        ).select_related("company", "invited_by")

    def perform_create(self, serializer):
        company = serializer.validated_data["company"]
        if not user_can_manage_company(self.request.user, company):
            raise exceptions.PermissionDenied("Non puoi invitare membri in questa azienda.")
        serializer.save(invited_by=self.request.user)
