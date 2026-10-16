from django.test import TestCase
from apps.accounts.models import User
from apps.companies.models import Company
from .access import accessible_properties, editable_properties
from .models import Owner, Property

class PropertyPermissionTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="property-manager",
            email="property-manager@example.com",
            password="strong-pass-123",
        )
        self.customer = User.objects.create_user(
            username="property-customer",
            email="property-customer@example.com",
            password="strong-pass-123",
        )
        self.company = Company.objects.create(
            name="Property Company",
            vat_number="IT10000000002",
            company_type=Company.Type.AGENCY,
            owner=self.manager,
        )
        self.property = Property.objects.create(
            company=self.company,
            created_by=self.manager,
            title="Immobile test",
            address="Via Test 1",
            municipality="Roma",
            province="RM",
        )
        Owner.objects.create(
            property=self.property,
            first_name="Cliente",
            last_name="Test",
            linked_user=self.customer,
            ownership_percentage=100,
        )

    def test_linked_customer_can_read_but_not_edit(self):
        self.assertTrue(accessible_properties(self.customer).filter(pk=self.property.pk).exists())
        self.assertFalse(editable_properties(self.customer).filter(pk=self.property.pk).exists())
