from django.test import TestCase
from apps.accounts.models import User
from .access import accessible_companies
from .models import Company, CompanyMembership

class CompanyAccessTest(TestCase):
    def test_member_can_access_company(self):
        owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="strong-pass-123",
        )
        member = User.objects.create_user(
            username="member",
            email="member@example.com",
            password="strong-pass-123",
        )
        company = Company.objects.create(
            name="Domus Demo",
            vat_number="IT00000000003",
            company_type=Company.Type.AGENCY,
            owner=owner,
        )
        CompanyMembership.objects.create(
            company=company,
            user=member,
            role=CompanyMembership.Role.OPERATOR,
        )
        self.assertTrue(accessible_companies(member).filter(id=company.id).exists())
