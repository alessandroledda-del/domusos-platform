from decimal import Decimal
from django.db import transaction, models
from django.db.models import Avg
from django.utils import timezone
from apps.notifications.models import Notification
from apps.notifications.tasks import send_email_task
from .models import Commission, PartnerAssignment, PartnerProfile, Payout

def partner_rank_score(partner):
    rating_component = Decimal(partner.rating or 0) * Decimal("12")
    sla_component = Decimal(partner.sla_compliance_rate or 0) * Decimal("0.30")
    experience_component = min(Decimal(partner.completed_assignments), Decimal("100")) * Decimal("0.10")
    featured_bonus = Decimal("5") if partner.is_featured else Decimal("0")
    return (rating_component + sla_component + experience_component + featured_bonus).quantize(Decimal("0.01"))

def rank_partners(queryset):
    return sorted(queryset, key=partner_rank_score, reverse=True)

@transaction.atomic
def assign_partner(case, partner, amount, user, order=None, due_at=None, notes=""):
    assignment = PartnerAssignment.objects.create(
        case=case,
        partner=partner,
        order=order,
        agreed_amount=amount,
        due_at=due_at,
        assigned_by=user,
        notes=notes,
    )

    Notification.objects.create(
        user=partner.user,
        title="Nuova pratica assegnata",
        message=f"Ti è stata proposta la pratica '{case.title}'.",
        level=Notification.Level.INFO,
    )

    send_email_task.delay(
        partner.user.email,
        f"Nuova pratica DomusOS: {case.title}",
        "partner_assignment",
        {
            "partner_name": partner.display_name,
            "case_title": case.title,
            "amount": str(amount),
            "due_at": due_at.isoformat() if due_at else "-",
        },
    )
    return assignment

@transaction.atomic
def complete_assignment(assignment):
    assignment.status = PartnerAssignment.Status.COMPLETED
    assignment.completed_at = timezone.now()
    assignment.save(update_fields=["status", "completed_at"])

    Commission.objects.update_or_create(
        assignment=assignment,
        defaults={
            "gross_amount": assignment.agreed_amount,
            "commission_rate": assignment.commission_rate,
            "platform_amount": assignment.commission_amount,
            "partner_amount": assignment.partner_net_amount,
            "status": Commission.Status.EARNED,
            "earned_at": timezone.now(),
        },
    )

    partner = assignment.partner
    completed = partner.assignments.filter(status=PartnerAssignment.Status.COMPLETED)
    partner.completed_assignments = completed.count()

    durations = []
    for item in completed.exclude(accepted_at=None).exclude(completed_at=None):
        durations.append(
            Decimal(str((item.completed_at - item.accepted_at).total_seconds() / 3600))
        )
    partner.average_completion_hours = (
        sum(durations, Decimal("0")) / len(durations)
        if durations else Decimal("0")
    )

    with_due = completed.exclude(due_at=None)
    if with_due.exists():
        on_time = with_due.filter(completed_at__lte=models.F("due_at")).count()
        partner.sla_compliance_rate = (
            Decimal(on_time) / Decimal(with_due.count()) * Decimal("100")
        ).quantize(Decimal("0.01"))

    partner.save(
        update_fields=[
            "completed_assignments",
            "average_completion_hours",
            "sla_compliance_rate",
            "updated_at",
        ]
    )
    return assignment

@transaction.atomic
def create_payout(partner, period_start, period_end):
    commissions = Commission.objects.filter(
        assignment__partner=partner,
        status=Commission.Status.EARNED,
        earned_at__date__gte=period_start,
        earned_at__date__lte=period_end,
    )
    amount = sum((item.partner_amount for item in commissions), Decimal("0.00"))
    payout = Payout.objects.create(
        partner=partner,
        amount=amount,
        period_start=period_start,
        period_end=period_end,
    )
    return payout, commissions
