from decimal import Decimal
from django.test import TestCase
from apps.accounts.models import User
from apps.orders.models import Order
from .services import build_global_metrics, create_global_snapshot

class AnalyticsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="analytics",
            email="analytics@example.com",
            password="strong-pass-123",
            is_staff=True,
        )

    def test_global_metrics_contract(self):
        Order.objects.create(
            customer=self.user,
            subtotal=Decimal("10.00"),
            vat_total=Decimal("2.20"),
            total=Decimal("12.20"),
        )
        metrics = build_global_metrics()
        self.assertEqual(metrics["orders"]["total"], 1)
        self.assertIn("operations", metrics)
        self.assertIn("compliance", metrics)

    def test_snapshot_creation(self):
        snapshot = create_global_snapshot(self.user)
        self.assertEqual(snapshot.scope, "GLOBAL")
        self.assertIn("orders", snapshot.metrics)
