from decimal import Decimal
from django.test import TestCase
from apps.accounts.models import User
from apps.companies.models import Company
from apps.properties.models import Property
from apps.workflows.models import Case
from .models import PartnerAssignment, PartnerProfile
from .services import assign_partner, complete_assignment, partner_rank_score

class MarketplaceTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin-marketplace",
            email="admin-marketplace@example.com",
            password="strong-pass-123",
            is_staff=True,
        )
        self.partner_user = User.objects.create_user(
            username="partner-marketplace",
            email="partner-marketplace@example.com",
            password="strong-pass-123",
        )
        self.partner = PartnerProfile.objects.create(
            user=self.partner_user,
            display_name="Studio Tecnico Demo",
            professional_type="Geometra",
            provinces=["RM"],
            status=PartnerProfile.Status.ACTIVE,
            rating=Decimal("4.50"),
            sla_compliance_rate=Decimal("95.00"),
            completed_assignments=20,
        )
        company = Company.objects.create(
            name="Marketplace Agency",
            vat_number="IT00000000009",
            company_type=Company.Type.AGENCY,
            owner=self.admin,
        )
        property_obj = Property.objects.create(
            company=company,
            created_by=self.admin,
            title="Immobile partner",
            address="Via Partner 1",
            municipality="Roma",
            province="RM",
        )
        self.case = Case.objects.create(
            property=property_obj,
            title="Pratica partner",
            service_type="Visura",
            created_by=self.admin,
        )

    def test_rank_score(self):
        score = partner_rank_score(self.partner)
        self.assertGreater(score, Decimal("70"))

    def test_assignment_commission(self):
        assignment = assign_partner(
            case=self.case,
            partner=self.partner,
            amount=Decimal("100.00"),
            user=self.admin,
        )
        self.assertEqual(assignment.commission_amount, Decimal("20.00"))
        self.assertEqual(assignment.partner_net_amount, Decimal("80.00"))

    def test_complete_assignment_creates_commission(self):
        assignment = assign_partner(
            case=self.case,
            partner=self.partner,
            amount=Decimal("100.00"),
            user=self.admin,
        )
        assignment.status = PartnerAssignment.Status.ACCEPTED
        from django.utils import timezone
        assignment.accepted_at = timezone.now()
        assignment.save()
        complete_assignment(assignment)
        self.assertTrue(hasattr(assignment, "commission"))
        self.assertEqual(assignment.commission.partner_amount, Decimal("80.00"))
