from rest_framework.routers import DefaultRouter
from .views import AnalyticsDashboardViewSet, AnalyticsSnapshotViewSet

router = DefaultRouter()
router.register("dashboard", AnalyticsDashboardViewSet, basename="analytics-dashboard")
router.register("snapshots", AnalyticsSnapshotViewSet, basename="analytics-snapshot")
urlpatterns = router.urls
