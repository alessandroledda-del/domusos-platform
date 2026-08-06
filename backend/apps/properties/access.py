from django.db.models import Q
from apps.companies.access import accessible_companies
from .models import Property

def accessible_properties(user):
    if not user.is_authenticated:
        return Property.objects.none()
    if user.is_superuser:
        return Property.objects.all()
    return Property.objects.filter(
        Q(company__in=accessible_companies(user)) |
        Q(owners__linked_user=user)
    ).distinct()
