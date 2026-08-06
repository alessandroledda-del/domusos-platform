from rest_framework import permissions, viewsets
from .models import Service, ServiceCategory
from .serializers import ServiceCategorySerializer, ServiceSerializer

class ReadOnlyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff or request.user.is_superuser

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [ReadOnlyOrAdmin]

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related("category")
        category = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        if category:
            queryset = queryset.filter(category__code=category)
        if featured in {"1", "true", "True"}:
            queryset = queryset.filter(is_featured=True)
        return queryset
