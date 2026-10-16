from django.conf import settings
from rest_framework import decorators, response, status, viewsets
from apps.orders.models import Order
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer
from .services import create_mock_payment, create_payment_intent, issue_invoice

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.filter(order__customer=self.request.user)
        if self.request.user.is_staff:
            queryset = Payment.objects.all()
        return queryset.select_related("order")

    @decorators.action(detail=False, methods=["post"])
    def create_intent(self, request):
        order_id = request.data.get("order")
        idempotency_key = request.headers.get("Idempotency-Key")
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            payment = create_payment_intent(order, request.user, idempotency_key)
        except Order.DoesNotExist:
            return response.Response({"detail": "Ordine non trovato."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as exc:
            return response.Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=False, methods=["post"])
    def mock_checkout(self, request):
        if not settings.DEBUG and not request.user.is_staff:
            return response.Response(
                {"detail": "Pagamento mock non disponibile in questo ambiente."},
                status=status.HTTP_403_FORBIDDEN,
            )
        order_id = request.data.get("order")
        succeed = request.data.get("succeed", True)
        try:
            queryset = Order.objects.all() if request.user.is_staff else Order.objects.filter(customer=request.user)
            order = queryset.get(id=order_id)
            payment = create_mock_payment(order, request.user, bool(succeed))
        except Order.DoesNotExist:
            return response.Response({"detail": "Ordine non trovato."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as exc:
            return response.Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )

class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        queryset = Invoice.objects.filter(order__customer=self.request.user)
        if self.request.user.is_staff:
            queryset = Invoice.objects.all()
        return queryset.select_related("order")

    @decorators.action(detail=False, methods=["post"])
    def issue(self, request):
        order_id = request.data.get("order")
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
        except Order.DoesNotExist:
            return response.Response({"detail": "Ordine non trovato."}, status=status.HTTP_404_NOT_FOUND)

        if order.status not in [Order.Status.PAID, Order.Status.IN_PROGRESS, Order.Status.COMPLETED]:
            return response.Response(
                {"detail": "La fattura può essere emessa solo per ordini pagati."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invoice = issue_invoice(
            order=order,
            customer_name=request.data.get("customer_name") or request.user.get_full_name() or request.user.email,
            customer_tax_code=request.data.get("customer_tax_code", ""),
            customer_address=request.data.get("customer_address", ""),
        )
        return response.Response(
            InvoiceSerializer(invoice, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
