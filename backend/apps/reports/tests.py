from django.test import TestCase
from apps.accounts.models import User
from apps.companies.models import Company
from apps.properties.models import Property
from .services import build_property_snapshot

class ReportSnapshotTest(TestCase):
    def test_snapshot_contains_score(self):
        user = User.objects.create_user(
            username="demo-report",
            email="report@example.com",
            password="strong-pass-123",
        )
        company = Company.objects.create(
            name="Agency Report",
            vat_number="IT00000000002",
            company_type=Company.Type.AGENCY,
            owner=user,
        )
        property_obj = Property.objects.create(
            company=company,
            created_by=user,
            title="Immobile Report",
            address="Via Test 1",
            municipality="Roma",
            province="RM",
            domus_score=65,
        )
        snapshot = build_property_snapshot(property_obj)
        self.assertEqual(snapshot["domus_score"], 65)
