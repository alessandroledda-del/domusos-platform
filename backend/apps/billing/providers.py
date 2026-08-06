import uuid
from dataclasses import dataclass
from django.conf import settings

@dataclass
class PaymentIntent:
    reference: str
    amount: str
    currency: str
    status: str
    client_secret: str = ""

class BasePaymentProvider:
    code = "BASE"

    def create_intent(self, order):
        raise NotImplementedError

class MockPaymentProvider(BasePaymentProvider):
    code = "MOCK"

    def create_intent(self, order):
        reference = f"mock_{uuid.uuid4().hex[:20]}"
        return PaymentIntent(
            reference=reference,
            amount=str(order.total),
            currency="EUR",
            status="requires_confirmation",
            client_secret=f"secret_{reference}",
        )

def get_payment_provider():
    provider = settings.PAYMENT_PROVIDER.upper()
    if provider == "MOCK":
        return MockPaymentProvider()
    raise ValueError(f"Provider pagamento non configurato: {provider}")
