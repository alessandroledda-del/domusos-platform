from decimal import Decimal
from django.test import TestCase
from apps.accounts.models import User
from apps.catalog.models import Service, ServiceCategory
from apps.orders.models import Order
from apps.orders.services import add_service_to_order, transition_order
from .models import Payment
from .services import create_mock_payment, issue_invoice

class BillingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="billing",
            email="billing@example.com",
            password="strong-pass-123",
        )
        category = ServiceCategory.objects.create(code="billing-cat", name="Billing")
        service = Service.objects.create(
            code="billing-service",
            category=category,
            name="Servizio fatturabile",
            short_description="Test",
            base_price=Decimal("20.00"),
            vat_rate=Decimal("22.00"),
        )
        self.order = Order.objects.create(customer=self.user)
        add_service_to_order(self.order, service)
        transition_order(self.order, Order.Status.AWAITING_PAYMENT, self.user)

    def test_mock_payment_marks_order_paid(self):
        payment = create_mock_payment(self.order, self.user)
        self.order.refresh_from_db()
        self.assertEqual(payment.status, Payment.Status.SUCCEEDED)
        self.assertEqual(self.order.status, Order.Status.PAID)

    def test_invoice_generation(self):
        create_mock_payment(self.order, self.user)
        invoice = issue_invoice(self.order, "Cliente Test", "RSSMRA80A01H501U", "Via Roma 1")
        self.assertEqual(invoice.total, self.order.total)
        self.assertTrue(invoice.pdf_file.name.endswith(".pdf"))
