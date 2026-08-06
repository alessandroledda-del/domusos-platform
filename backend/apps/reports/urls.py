from rest_framework.routers import DefaultRouter
from .views import PropertyReportViewSet

router = DefaultRouter()
router.register("", PropertyReportViewSet, basename="report")
urlpatterns = router.urls
