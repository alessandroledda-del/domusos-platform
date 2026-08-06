from django.urls import path
from rest_framework.routers import DefaultRouter
from .partner import PartnerPortalView
from .views import CaseViewSet, TaskViewSet

router = DefaultRouter()
router.register("cases", CaseViewSet, basename="case")
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("partner-portal/", PartnerPortalView.as_view()),
] + router.urls
