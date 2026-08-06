from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory, force_authenticate
from apps.accounts.models import User
from .readiness import ReadinessView

class ReadinessTest(TestCase):
    @override_settings(
        DEBUG=False,
        SECRET_KEY="secure-test-secret",
        ALLOWED_HOSTS=["testserver"],
        ANTIVIRUS_ENABLED=True,
        USE_S3=True,
        DEFAULT_FROM_EMAIL="test@example.com",
    )
    def test_readiness_requires_catalog(self):
        user = User.objects.create_user(
            username="admin-ready",
            email="admin-ready@example.com",
            password="strong-pass-123",
            is_staff=True,
            is_superuser=True,
        )
        request = APIRequestFactory().get("/api/readiness/")
        force_authenticate(request, user=user)
        response = ReadinessView.as_view()(request)
        self.assertEqual(response.status_code, 503)
