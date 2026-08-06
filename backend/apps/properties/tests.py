from django.test import TestCase
from apps.accounts.models import User
from apps.companies.models import Company
from .models import Property
from .services import calculate_domus_score

class PropertyScoreTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="demo", email="demo@example.com", password="strong-pass-123")
        company = Company.objects.create(
            name="Demo Agency",
            vat_number="IT00000000001",
            company_type=Company.Type.AGENCY,
            owner=user,
        )
        self.property = Property.objects.create(
            company=company,
            created_by=user,
            title="Casa Demo",
            address="Via Roma 1",
            municipality="Roma",
            province="RM",
            cadastral_sheet="10",
            cadastral_particle="20",
        )

    def test_score_uses_cadastral_fields(self):
        self.assertEqual(calculate_domus_score(self.property), 20)
