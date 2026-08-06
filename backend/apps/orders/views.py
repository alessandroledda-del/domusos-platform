from django.db.models import Count, Sum
from rest_framework import decorators, permissions, response, status, viewsets
from .models import Order
from .serializers import CreateOrderSerializer, OrderSerializer
from .services import transition_order

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = (
            Order.objects.filter(customer=self.request.user)
            .prefetch_related("items__service", "status_events")
        )
        if self.request.user.is_staff:
            queryset = Order.objects.all().prefetch_related("items__service", "status_events")
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        transition_order(order, Order.Status.AWAITING_PAYMENT, request.user)
        return response.Response(
            OrderSerializer(order, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(detail=True, methods=["post"])
    def transition(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")
        note = request.data.get("note", "")
        try:
            transition_order(order, new_status, request.user, note)
        except ValueError as exc:
            return response.Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(OrderSerializer(order).data)

class OrderDashboardViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Order.objects.all() if request.user.is_staff else Order.objects.filter(customer=request.user)
        totals = queryset.aggregate(
            orders=Count("id"),
            revenue=Sum("total"),
        )
        return response.Response({
            "orders_total": totals["orders"] or 0,
            "revenue_total": totals["revenue"] or 0,
            "awaiting_payment": queryset.filter(status=Order.Status.AWAITING_PAYMENT).count(),
            "in_progress": queryset.filter(status=Order.Status.IN_PROGRESS).count(),
            "completed": queryset.filter(status=Order.Status.COMPLETED).count(),
            "sla_at_risk": queryset.filter(
                status__in=[Order.Status.PAID, Order.Status.IN_PROGRESS],
                sla_due_at__isnull=False,
            ).count(),
        })
