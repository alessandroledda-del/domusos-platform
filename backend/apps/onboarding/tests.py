from django.test import TestCase
from apps.accounts.models import User
from .services import compute_onboarding

class OnboardingTest(TestCase):
    def test_new_user_has_zero_core_progress(self):
        user = User.objects.create_user(
            username="onboarding",
            email="onboarding@example.com",
            password="strong-pass-123",
        )
        progress = compute_onboarding(user)
        self.assertFalse(progress.organization_created)
        self.assertFalse(progress.first_property_created)
        self.assertFalse(progress.completed)
