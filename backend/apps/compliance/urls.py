from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CertificateViewSet,
    ComplianceDashboardView,
    FindingViewSet,
    PublicCertificateVerifyView,
    VerificationRunViewSet,
)

router = DefaultRouter()
router.register("verifications", VerificationRunViewSet, basename="verification")
router.register("findings", FindingViewSet, basename="finding")
router.register("certificates", CertificateViewSet, basename="certificate")

urlpatterns = [
    path("dashboard/", ComplianceDashboardView.as_view()),
    path("public/<str:public_code>/", PublicCertificateVerifyView.as_view()),
] + router.urls
