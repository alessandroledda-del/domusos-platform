from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, CompanyViewSet, PropertyViewSet

# Create a router and register viewsets
router = SimpleRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'properties', PropertyViewSet, basename='property')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
