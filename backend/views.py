from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import CompanyFilter, PropertyFilter, UserFilter
from .models import Company, Property, User
from .pagination import StandardResultsSetPagination
from .permissions import IsAdminOrManager, IsAdminOrManagerOrReadOnly
from .serializers import (
    CompanyDetailSerializer,
    CompanySerializer,
    PropertyCreateUpdateSerializer,
    PropertyDetailSerializer,
    PropertySerializer,
    UserDetailSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user management."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = UserFilter
    search_fields = ['email', 'nome', 'cognome']
    ordering_fields = ['created_at', 'email', 'nome', 'cognome']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrManager]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'me':
            return UserDetailSerializer
        return UserSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        if request.user != user and request.user.ruolo not in {'admin', 'manager'}:
            return Response({'detail': 'You do not have permission to change this password.'}, status=403)

        password = request.data.get('password')
        if not password:
            return Response({'password': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save(update_fields=['password'])
        return Response({'status': 'password set'})

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for company management."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = CompanyFilter
    search_fields = ['ragione_sociale', 'partita_iva', 'email']
    ordering_fields = ['created_at', 'ragione_sociale', 'tipo_cliente']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer

    @action(detail=True, methods=['get'])
    def properties(self, request, pk=None):
        company = self.get_object()
        serializer = PropertySerializer(company.properties.all(), many=True)
        return Response(serializer.data)


class PropertyViewSet(viewsets.ModelViewSet):
    """ViewSet for property management."""

    permission_classes = [IsAdminOrManagerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['indirizzo', 'comune', 'provincia', 'company__ragione_sociale']
    ordering_fields = ['created_at', 'domus_score', 'comune', 'provincia']

    def get_queryset(self):
        return Property.objects.select_related('company').all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PropertyDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return PropertyCreateUpdateSerializer
        return PropertySerializer

    @action(detail=False, methods=['get'])
    def by_company(self, request):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({'error': 'company_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        company = get_object_or_404(Company, id=company_id)
        serializer = PropertySerializer(company.properties.select_related('company').all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_score(self, request, pk=None):
        property_obj = self.get_object()
        score = request.data.get('domus_score')
        if score is None:
            return Response({'domus_score': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            property_obj.domus_score = float(score)
            property_obj.save(update_fields=['domus_score'])
        except (TypeError, ValueError):
            return Response({'domus_score': 'Invalid score value.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PropertyDetailSerializer(property_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        property_obj = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Property.STATUS_CHOICES):
            return Response(
                {'status': f'Invalid status. Must be one of: {", ".join(dict(Property.STATUS_CHOICES).keys())}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        property_obj.status = new_status
        property_obj.save(update_fields=['status'])
        serializer = PropertyDetailSerializer(property_obj)
        return Response(serializer.data)
