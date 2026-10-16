from django.test import TestCase
from apps.accounts.models import User
from .access import user_can_admin_company, user_can_manage_company
from .models import Company, CompanyMembership

class CompanyPermissionTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="company-owner",
            email="company-owner@example.com",
            password="strong-pass-123",
        )
        self.viewer = User.objects.create_user(
            username="company-viewer",
            email="company-viewer@example.com",
            password="strong-pass-123",
        )
        self.company = Company.objects.create(
            name="Company Test",
            vat_number="IT10000000001",
            company_type=Company.Type.AGENCY,
            owner=self.owner,
        )
        CompanyMembership.objects.create(
            company=self.company,
            user=self.viewer,
            role=CompanyMembership.Role.VIEWER,
        )

    def test_owner_can_administer_company(self):
        self.assertTrue(user_can_admin_company(self.owner, self.company))

    def test_viewer_cannot_manage_company(self):
        self.assertFalse(user_can_manage_company(self.viewer, self.company))
