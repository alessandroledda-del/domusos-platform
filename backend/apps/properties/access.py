from django.db.models import Q
from apps.companies.access import accessible_companies, editable_companies, manageable_companies
from .models import Property

def accessible_properties(user):
    if not user.is_authenticated:
        return Property.objects.none()
    if user.is_superuser:
        return Property.objects.all()
    return Property.objects.filter(
        Q(company__in=accessible_companies(user))
        | Q(owners__linked_user=user)
    ).distinct()

def editable_properties(user):
    if not user.is_authenticated:
        return Property.objects.none()
    if user.is_superuser:
        return Property.objects.all()
    return Property.objects.filter(company__in=editable_companies(user)).distinct()

def manageable_properties(user):
    if not user.is_authenticated:
        return Property.objects.none()
    if user.is_superuser:
        return Property.objects.all()
    return Property.objects.filter(company__in=manageable_companies(user)).distinct()
