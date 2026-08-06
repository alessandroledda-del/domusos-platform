from apps.companies.models import Company
from apps.documents.models import Document
from apps.orders.models import Order
from apps.properties.models import Property
from apps.compliance.models import VerificationRun
from .models import OnboardingProgress

def compute_onboarding(user):
    progress, _ = OnboardingProgress.objects.get_or_create(user=user)

    progress.organization_created = Company.objects.filter(
        owner=user
    ).exists() or user.company_memberships.filter(is_active=True).exists()

    progress.profile_completed = bool(
        user.first_name and user.last_name and user.phone
    )

    progress.first_property_created = Property.objects.filter(
        created_by=user
    ).exists()

    progress.first_document_uploaded = Document.objects.filter(
        uploaded_by=user
    ).exists()

    progress.first_service_ordered = Order.objects.filter(
        customer=user
    ).exclude(status=Order.Status.DRAFT).exists()

    progress.first_verification_run = VerificationRun.objects.filter(
        requested_by=user
    ).exists()

    progress.refresh_completion()
    return progress
