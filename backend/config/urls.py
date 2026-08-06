from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .health import health_check
from .metrics import metrics_view
from .readiness import readiness_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health_check, name="health"),
    path("api/metrics/", metrics_view, name="metrics"),
    path("api/readiness/", readiness_view, name="readiness"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/companies/", include("apps.companies.urls")),
    path("api/properties/", include("apps.properties.urls")),
    path("api/documents/", include("apps.documents.urls")),
    path("api/workflows/", include("apps.workflows.urls")),
    path("api/audit/", include("apps.audit.urls")),
    path("api/reports/", include("apps.reports.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/search/", include("apps.search.urls")),
    path("api/catalog/", include("apps.catalog.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/billing/", include("apps.billing.urls")),
    path("api/integrations/", include("apps.integrations.urls")),
    path("api/compliance/", include("apps.compliance.urls")),
    path("api/analytics/", include("apps.analytics.urls")),
    path("api/marketplace/", include("apps.marketplace.urls")),
    path("api/onboarding/", include("apps.onboarding.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
