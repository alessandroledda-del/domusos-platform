from datetime import timedelta
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from apps.integrations.tasks import publish_event
from apps.notifications.models import Notification
from apps.notifications.tasks import send_email_task
from apps.properties.services import refresh_domus_score
from .models import Finding, VerificationCertificate, VerificationRun
from .rules import DEFAULT_RULES

SEVERITY_PENALTIES = {
    "INFO": 0,
    "LOW": 3,
    "MEDIUM": 7,
    "HIGH": 12,
    "CRITICAL": 25,
}

def determine_verified_level(score, findings):
    open_findings = [item for item in findings if not item.passed]
    severities = {item.severity for item in open_findings}

    if "CRITICAL" in severities:
        return "NOT_VERIFIED"
    if score >= 90 and not severities.intersection({"HIGH", "CRITICAL"}):
        return "VERIFIED_PLUS"
    if score >= 75 and "HIGH" not in severities:
        return "VERIFIED"
    if score >= 55:
        return "CONDITIONAL"
    return "NOT_VERIFIED"

@transaction.atomic
def run_verification(property_obj, user):
    verification = VerificationRun.objects.create(
        property=property_obj,
        requested_by=user,
        status=VerificationRun.Status.RUNNING,
    )

    try:
        results = [rule.evaluate(property_obj) for rule in DEFAULT_RULES]
        total_weight = sum(result.weight for result in results)
        passed_weight = sum(result.weight for result in results if result.passed)
        score = round((passed_weight / total_weight) * 100) if total_weight else 0

        failed_results = [result for result in results if not result.passed]
        for result in failed_results:
            Finding.objects.create(
                verification=verification,
                property=property_obj,
                rule_code=result.code,
                title=result.title,
                description=result.description,
                severity=result.severity,
                evidence=result.evidence,
            )

        verification.score = score
        verification.passed_rules = sum(1 for result in results if result.passed)
        verification.warning_rules = sum(
            1 for result in failed_results if result.severity in {"INFO", "LOW", "MEDIUM"}
        )
        verification.failed_rules = sum(
            1 for result in failed_results if result.severity in {"HIGH", "CRITICAL"}
        )
        verification.summary = {
            "verified_level": determine_verified_level(score, results),
            "rules": [
                {
                    "code": result.code,
                    "title": result.title,
                    "passed": result.passed,
                    "severity": result.severity,
                    "description": result.description,
                    "weight": result.weight,
                }
                for result in results
            ],
        }
        verification.status = VerificationRun.Status.COMPLETED
        verification.completed_at = timezone.now()
        verification.save()

        property_obj.domus_score = score
        property_obj.status = (
            "VERIFIED"
            if verification.summary["verified_level"] in {"VERIFIED", "VERIFIED_PLUS"}
            else "ISSUE"
            if verification.failed_rules
            else "ANALYSIS"
        )
        property_obj.save(update_fields=["domus_score", "status", "updated_at"])

        Notification.objects.create(
            user=user,
            title=f"Verifica completata: {property_obj.title}",
            message=(
                f"Esito {verification.summary['verified_level']} "
                f"con punteggio {verification.score}/100."
            ),
            level=(
                Notification.Level.SUCCESS
                if verification.summary["verified_level"] in {"VERIFIED", "VERIFIED_PLUS"}
                else Notification.Level.WARNING
            ),
        )

        publish_event(
            "property.verification_completed",
            {
                "verification_id": verification.id,
                "property_id": property_obj.id,
                "score": verification.score,
                "verified_level": verification.summary["verified_level"],
                "failed_rules": verification.failed_rules,
            },
        )

        return verification
    except Exception:
        verification.status = VerificationRun.Status.FAILED
        verification.completed_at = timezone.now()
        verification.save(update_fields=["status", "completed_at"])
        raise

def build_certificate_pdf(certificate):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(width / 2, height - 70, "DOMUS VERIFIED")

    pdf.setFont("Helvetica", 11)
    y = height - 120
    lines = [
        f"Codice verifica: {certificate.public_code}",
        f"Immobile: {certificate.property.title}",
        f"Indirizzo: {certificate.property.address}",
        f"Comune: {certificate.property.municipality} ({certificate.property.province})",
        f"Livello: {certificate.verified_level}",
        f"Punteggio: {certificate.score}/100",
        f"Data emissione: {certificate.issued_at.strftime('%d/%m/%Y %H:%M') if certificate.issued_at else '-'}",
        f"Scadenza: {certificate.expires_at.strftime('%d/%m/%Y') if certificate.expires_at else '-'}",
        "",
        "Avvertenza:",
        "Questo certificato rappresenta una pre-verifica documentale DomusOS.",
        "Non sostituisce attestazioni, perizie o verifiche di professionisti e pubbliche autorità.",
    ]
    for line in lines:
        pdf.drawString(55, y, line[:105])
        y -= 20

    pdf.save()
    buffer.seek(0)
    return buffer.read()

@transaction.atomic
def issue_certificate(verification, user):
    if verification.status != VerificationRun.Status.COMPLETED:
        raise ValueError("La verifica non è completata.")

    level = verification.summary.get("verified_level", "NOT_VERIFIED")
    if level not in {"VERIFIED", "VERIFIED_PLUS"}:
        raise ValueError("L'immobile non soddisfa i requisiti Domus Verified.")

    certificate, created = VerificationCertificate.objects.get_or_create(
        verification=verification,
        defaults={
            "property": verification.property,
            "issued_by": user,
            "verified_level": level,
            "score": verification.score,
            "snapshot": verification.summary,
            "expires_at": timezone.now() + timedelta(days=90),
        },
    )

    if created or not certificate.pdf_file:
        content = build_certificate_pdf(certificate)
        certificate.pdf_file.save(
            f"{certificate.public_code}.pdf",
            ContentFile(content),
            save=True,
        )

    publish_event(
        "property.certificate_issued",
        {
            "certificate_id": certificate.id,
            "public_code": certificate.public_code,
            "property_id": certificate.property_id,
            "verified_level": certificate.verified_level,
            "score": certificate.score,
        },
    )
    return certificate
