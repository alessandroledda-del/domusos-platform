from django.test import TestCase
from apps.accounts.models import User
from apps.orders.models import Order
from .services import create_payment_intent

class PaymentIdempotencyTest(TestCase):
    def test_same_order_and_key_returns_same_payment(self):
        user = User.objects.create_user(
            username="payment-user",
            email="payment-user@example.com",
            password="strong-pass-123",
        )
        order = Order.objects.create(
            customer=user,
            status=Order.Status.AWAITING_PAYMENT,
            total="10.00",
        )
        first = create_payment_intent(order, user, "request-123")
        second = create_payment_intent(order, user, "request-123")
        self.assertEqual(first.pk, second.pk)
