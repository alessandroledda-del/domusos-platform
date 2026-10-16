from django.test import TestCase
from rest_framework.test import APIRequestFactory
from apps.accounts.models import User
from .models import Order
from .serializers import OrderSerializer

class OrderSecurityTest(TestCase):
    def test_status_and_relations_are_read_only_after_creation(self):
        user = User.objects.create_user(
            username="order-user",
            email="order-user@example.com",
            password="strong-pass-123",
        )
        order = Order.objects.create(customer=user)
        request = APIRequestFactory().patch("/")
        request.user = user
        serializer = OrderSerializer(
            order,
            data={"status": Order.Status.PAID, "company": 999, "property": 999},
            partial=True,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        saved = serializer.save()
        self.assertEqual(saved.status, Order.Status.DRAFT)
        self.assertIsNone(saved.company_id)
        self.assertIsNone(saved.property_id)
