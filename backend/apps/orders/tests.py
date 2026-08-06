from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.accounts.models import User
from apps.catalog.models import Service, ServiceCategory
from .models import Order
from .services import add_service_to_order, calculate_sla_due, transition_order

class OrderServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="buyer",
            email="buyer@example.com",
            password="strong-pass-123",
        )
        category = ServiceCategory.objects.create(code="catasto-test", name="Catasto Test")
        self.service = Service.objects.create(
            code="visura-test",
            category=category,
            name="Visura test",
            short_description="Test",
            base_price=Decimal("10.00"),
            vat_rate=Decimal("22.00"),
            sla_hours=12,
        )
        self.order = Order.objects.create(customer=self.user)

    def test_add_service_recalculates_totals(self):
        add_service_to_order(self.order, self.service)
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal, Decimal("10.00"))
        self.assertEqual(self.order.vat_total, Decimal("2.20"))
        self.assertEqual(self.order.total, Decimal("12.20"))

    def test_sla_uses_longest_item(self):
        add_service_to_order(self.order, self.service)
        due = calculate_sla_due(self.order)
        self.assertGreaterEqual(due, timezone.now() + timedelta(hours=11, minutes=59))

    def test_order_transition(self):
        add_service_to_order(self.order, self.service)
        transition_order(self.order, Order.Status.AWAITING_PAYMENT, self.user)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.AWAITING_PAYMENT)
