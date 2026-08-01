from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CompanyViewSet, PropertyViewSet, UserViewSet


router = SimpleRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'properties', PropertyViewSet, basename='property')


urlpatterns = [
    path('', include(router.urls)),
]
