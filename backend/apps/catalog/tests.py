from decimal import Decimal
from django.test import TestCase
from .models import Service, ServiceCategory

class ServicePriceTest(TestCase):
    def test_gross_price(self):
        category = ServiceCategory.objects.create(code="test", name="Test")
        service = Service.objects.create(
            code="service-test",
            category=category,
            name="Servizio test",
            short_description="Test",
            base_price=Decimal("100.00"),
            vat_rate=Decimal("22.00"),
        )
        self.assertEqual(service.gross_price, Decimal("122.00"))
