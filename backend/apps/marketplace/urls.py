from rest_framework.routers import DefaultRouter
from .views import (
    CommissionViewSet,
    MarketplaceDashboardViewSet,
    PartnerAssignmentViewSet,
    PartnerProfileViewSet,
    PartnerServiceViewSet,
    PayoutViewSet,
)

router = DefaultRouter()
router.register("partners", PartnerProfileViewSet, basename="partner-profile")
router.register("services", PartnerServiceViewSet, basename="partner-service")
router.register("assignments", PartnerAssignmentViewSet, basename="partner-assignment")
router.register("commissions", CommissionViewSet, basename="commission")
router.register("payouts", PayoutViewSet, basename="payout")
router.register("dashboard", MarketplaceDashboardViewSet, basename="marketplace-dashboard")
urlpatterns = router.urls
