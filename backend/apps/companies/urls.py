from rest_framework.routers import DefaultRouter
from .views import (
    CompanyInvitationViewSet,
    CompanyMembershipViewSet,
    CompanyViewSet,
)

router = DefaultRouter()
router.register("organizations", CompanyViewSet, basename="company")
router.register("memberships", CompanyMembershipViewSet, basename="membership")
router.register("invitations", CompanyInvitationViewSet, basename="invitation")
urlpatterns = router.urls
