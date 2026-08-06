from decimal import Decimal
from django.test import TestCase
from apps.accounts.models import User
from apps.companies.models import Company
from apps.documents.models import Document
from apps.properties.models import Owner, Property
from .rules import CadastralIdentityRule, OwnershipQuotaRule
from .services import determine_verified_level, run_verification

class ComplianceRulesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="compliance",
            email="compliance@example.com",
            password="strong-pass-123",
        )
        self.company = Company.objects.create(
            name="Compliance Agency",
            vat_number="IT00000000008",
            company_type=Company.Type.AGENCY,
            owner=self.user,
        )
        self.property = Property.objects.create(
            company=self.company,
            created_by=self.user,
            title="Immobile verifica",
            address="Via Verifica 1",
            municipality="Roma",
            province="RM",
            cadastral_sheet="10",
            cadastral_particle="20",
            cadastral_subaltern="3",
        )

    def test_cadastral_rule_passes(self):
        result = CadastralIdentityRule().evaluate(self.property)
        self.assertTrue(result.passed)

    def test_ownership_rule_requires_100_percent(self):
        Owner.objects.create(
            property=self.property,
            first_name="Mario",
            last_name="Rossi",
            ownership_percentage=Decimal("50"),
        )
        result = OwnershipQuotaRule().evaluate(self.property)
        self.assertFalse(result.passed)

    def test_verified_level(self):
        class Result:
            def __init__(self, passed, severity):
                self.passed = passed
                self.severity = severity
        results = [Result(True, "LOW"), Result(False, "MEDIUM")]
        self.assertEqual(determine_verified_level(80, results), "VERIFIED")

    def test_run_verification_creates_findings(self):
        verification = run_verification(self.property, self.user)
        self.assertEqual(verification.status, "COMPLETED")
        self.assertGreater(verification.findings.count(), 0)
