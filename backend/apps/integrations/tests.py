from django.test import SimpleTestCase
from .signatures import sign_payload, verify_signature

class SignatureTest(SimpleTestCase):
    def test_sign_and_verify(self):
        payload = {"event": "order.status_changed", "id": 10}
        secret = "secret"
        signature = sign_payload(payload, secret)
        self.assertTrue(verify_signature(payload, secret, signature))
        self.assertFalse(verify_signature(payload, secret, "invalid"))
