from django.urls import path
from rest_framework.routers import DefaultRouter
from .customer import CustomerPortalView
from .dashboard import DashboardView
from .views import OwnerViewSet, PropertyViewSet

router = DefaultRouter()
router.register("items", PropertyViewSet, basename="property")
router.register("owners", OwnerViewSet, basename="owner")

urlpatterns = [
    path("dashboard/", DashboardView.as_view()),
    path("customer-portal/", CustomerPortalView.as_view()),
] + router.urls
