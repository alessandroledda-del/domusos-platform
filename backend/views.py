from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .models import User, Company, Property
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    CompanySerializer,
    CompanyDetailSerializer,
    PropertySerializer,
    PropertyDetailSerializer,
    PropertyCreateUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management
    - list: Get all users
    - create: Create a new user
    - retrieve: Get a specific user
    - update: Update a user
    - destroy: Delete a user
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Use DetailSerializer for retrieve action"""
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to handle password field"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        """Set a new password for the user"""
        user = self.get_object()
        password = request.data.get('password')
        
        if not password:
            return Response(
                {'password': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(password)
        user.save()
        return Response({'status': 'password set'})
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Company management
    - list: Get all companies
    - create: Create a new company
    - retrieve: Get a specific company
    - update: Update a company
    - destroy: Delete a company
    """
    
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Use DetailSerializer for retrieve action"""
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer
    
    @action(detail=True, methods=['get'])
    def properties(self, request, pk=None):
        """Get all properties for a specific company"""
        company = self.get_object()
        properties = company.properties.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)


class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Property management
    - list: Get all properties
    - create: Create a new property
    - retrieve: Get a specific property
    - update: Update a property
    - destroy: Delete a property
    """
    
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Use different serializers based on action"""
        if self.action == 'retrieve':
            return PropertyDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PropertyCreateUpdateSerializer
        return PropertySerializer
    
    def get_queryset(self):
        """Filter properties by company if provided"""
        queryset = Property.objects.all()
        company_id = self.request.query_params.get('company_id', None)
        
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_company(self, request):
        """Get properties filtered by company"""
        company_id = request.query_params.get('company_id')
        
        if not company_id:
            return Response(
                {'error': 'company_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        company = get_object_or_404(Company, id=company_id)
        properties = company.properties.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_score(self, request, pk=None):
        """Update the Domus Score for a property"""
        property_obj = self.get_object()
        score = request.data.get('domus_score')
        
        if score is None:
            return Response(
                {'domus_score': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            property_obj.domus_score = float(score)
            property_obj.save()
            serializer = PropertyDetailSerializer(property_obj)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'domus_score': 'Invalid score value.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update the status for a property"""
        property_obj = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Property.STATUS_CHOICES):
            return Response(
                {'status': f'Invalid status. Must be one of: {", ".join(dict(Property.STATUS_CHOICES).keys())}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        property_obj.status = new_status
        property_obj.save()
        serializer = PropertyDetailSerializer(property_obj)
        return Response(serializer.data)
