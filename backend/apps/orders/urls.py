from rest_framework.routers import DefaultRouter
from .views import OrderDashboardViewSet, OrderViewSet

router = DefaultRouter()
router.register("dashboard", OrderDashboardViewSet, basename="order-dashboard")
router.register("", OrderViewSet, basename="order")
urlpatterns = router.urls
