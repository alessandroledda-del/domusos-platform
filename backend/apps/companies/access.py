from django.db.models import Q
from .models import Company, CompanyMembership

def accessible_companies(user):
    if not user.is_authenticated:
        return Company.objects.none()
    if user.is_superuser:
        return Company.objects.all()
    return Company.objects.filter(
        Q(owner=user) | Q(memberships__user=user, memberships__is_active=True)
    ).distinct()

def user_can_manage_company(user, company):
    if user.is_superuser or company.owner_id == user.id:
        return True
    return company.memberships.filter(
        user=user,
        is_active=True,
        role__in=[
            CompanyMembership.Role.ADMIN,
            CompanyMembership.Role.MANAGER,
        ],
    ).exists()
