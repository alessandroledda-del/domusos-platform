from django.core import mail
from django.test import TestCase, override_settings
from .emailing import send_templated_email

class EmailTest(TestCase):
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_order_email(self):
        sent = send_templated_email(
            recipient="client@example.com",
            subject="Ordine aggiornato",
            template_name="order_status",
            context={
                "order_number": "DOM-2026-000001",
                "status_label": "Pagato",
                "total": "49.90",
            },
        )
        self.assertEqual(sent, 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("DOM-2026-000001", mail.outbox[0].body)
