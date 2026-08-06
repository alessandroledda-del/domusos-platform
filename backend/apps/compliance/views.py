from django.utils import timezone
from rest_framework import decorators, permissions, response, status, views, viewsets
from apps.properties.access import accessible_properties
from .models import Finding, VerificationCertificate, VerificationRun
from .serializers import (
    FindingSerializer,
    VerificationCertificateSerializer,
    VerificationRunSerializer,
)
from .services import issue_certificate, run_verification

class VerificationRunViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VerificationRunSerializer

    def get_queryset(self):
        return VerificationRun.objects.filter(
            property__in=accessible_properties(self.request.user)
        ).prefetch_related("findings")

    @decorators.action(detail=False, methods=["post"])
    def run(self, request):
        property_id = request.data.get("property")
        try:
            property_obj = accessible_properties(request.user).get(id=property_id)
        except Exception:
            return response.Response(
                {"detail": "Immobile non trovato."},
                status=status.HTTP_404_NOT_FOUND,
            )

        verification = run_verification(property_obj, request.user)
        return response.Response(
            VerificationRunSerializer(verification).data,
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(detail=True, methods=["post"])
    def issue_certificate(self, request, pk=None):
        verification = self.get_object()
        try:
            certificate = issue_certificate(verification, request.user)
        except ValueError as exc:
            return response.Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response.Response(
            VerificationCertificateSerializer(certificate, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class FindingViewSet(viewsets.ModelViewSet):
    serializer_class = FindingSerializer
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return Finding.objects.filter(
            property__in=accessible_properties(self.request.user)
        ).select_related("verification", "property")

    def perform_update(self, serializer):
        instance = serializer.instance
        new_status = serializer.validated_data.get("status", instance.status)
        extra = {}
        if new_status == Finding.Status.RESOLVED:
            extra = {
                "resolved_by": self.request.user,
                "resolved_at": timezone.now(),
            }
        serializer.save(**extra)

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VerificationCertificateSerializer

    def get_queryset(self):
        return VerificationCertificate.objects.filter(
            property__in=accessible_properties(self.request.user)
        )

class PublicCertificateVerifyView(views.APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, public_code):
        try:
            certificate = VerificationCertificate.objects.select_related("property").get(
                public_code=public_code
            )
        except VerificationCertificate.DoesNotExist:
            return response.Response(
                {"valid": False, "detail": "Certificato non trovato."},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_expired = certificate.expires_at and certificate.expires_at <= timezone.now()
        valid = certificate.status == VerificationCertificate.Status.VALID and not is_expired

        return response.Response({
            "valid": valid,
            "public_code": certificate.public_code,
            "status": "EXPIRED" if is_expired else certificate.status,
            "property": {
                "title": certificate.property.title,
                "municipality": certificate.property.municipality,
                "province": certificate.property.province,
            },
            "verified_level": certificate.verified_level,
            "score": certificate.score,
            "issued_at": certificate.issued_at,
            "expires_at": certificate.expires_at,
            "disclaimer": (
                "Pre-verifica documentale DomusOS. "
                "Non sostituisce verifiche professionali o pubbliche."
            ),
        })

class ComplianceDashboardView(views.APIView):
    def get(self, request):
        properties = accessible_properties(request.user)
        verifications = VerificationRun.objects.filter(property__in=properties)
        findings = Finding.objects.filter(property__in=properties)

        return response.Response({
            "properties_total": properties.count(),
            "verified_properties": properties.filter(status="VERIFIED").count(),
            "properties_with_issues": properties.filter(status="ISSUE").count(),
            "verification_runs": verifications.count(),
            "open_findings": findings.filter(status__in=["OPEN", "ACKNOWLEDGED"]).count(),
            "critical_findings": findings.filter(
                status__in=["OPEN", "ACKNOWLEDGED"],
                severity="CRITICAL",
            ).count(),
            "high_findings": findings.filter(
                status__in=["OPEN", "ACKNOWLEDGED"],
                severity="HIGH",
            ).count(),
        })
