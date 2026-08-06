from decimal import Decimal
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User
from apps.catalog.models import Service
from apps.companies.models import Company, CompanyMembership
from apps.marketplace.models import PartnerProfile, PartnerService
from apps.orders.models import Order
from apps.orders.services import add_service_to_order, transition_order
from apps.properties.models import Owner, Property
from apps.workflows.models import Case

class Command(BaseCommand):
    help = "Crea un ambiente demo DomusOS con utenti e dati di esempio."

    def handle(self, *args, **options):
        call_command("seed_catalog")

        admin, _ = User.objects.get_or_create(
            email="admin@demo.domusos.local",
            defaults={
                "username": "domus_admin",
                "first_name": "Admin",
                "last_name": "DomusOS",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("DomusOS-Demo-2026!")
        admin.save()

        agency_user, _ = User.objects.get_or_create(
            email="agenzia@demo.domusos.local",
            defaults={
                "username": "agenzia_demo",
                "first_name": "Anna",
                "last_name": "Agenzia",
                "role": User.Role.AGENCY,
                "phone": "+390000000001",
            },
        )
        agency_user.set_password("DomusOS-Demo-2026!")
        agency_user.save()

        client, _ = User.objects.get_or_create(
            email="cliente@demo.domusos.local",
            defaults={
                "username": "cliente_demo",
                "first_name": "Mario",
                "last_name": "Rossi",
                "role": User.Role.CLIENT,
                "phone": "+390000000002",
            },
        )
        client.set_password("DomusOS-Demo-2026!")
        client.save()

        partner_user, _ = User.objects.get_or_create(
            email="partner@demo.domusos.local",
            defaults={
                "username": "partner_demo",
                "first_name": "Giulia",
                "last_name": "Tecnica",
                "role": User.Role.TECHNICIAN,
                "phone": "+390000000003",
            },
        )
        partner_user.set_password("DomusOS-Demo-2026!")
        partner_user.save()

        company, _ = Company.objects.get_or_create(
            vat_number="IT99999999999",
            defaults={
                "name": "Agenzia Demo DomusOS",
                "company_type": Company.Type.AGENCY,
                "owner": agency_user,
            },
        )
        CompanyMembership.objects.get_or_create(
            company=company,
            user=agency_user,
            defaults={"role": CompanyMembership.Role.ADMIN},
        )

        property_obj, _ = Property.objects.get_or_create(
            company=company,
            title="Appartamento Demo Roma",
            defaults={
                "created_by": agency_user,
                "address": "Via Demo 10",
                "municipality": "Roma",
                "province": "RM",
                "postal_code": "00100",
                "cadastral_sheet": "123",
                "cadastral_particle": "456",
                "cadastral_subaltern": "7",
                "cadastral_category": "A/2",
                "status": Property.Status.ANALYSIS,
            },
        )

        Owner.objects.get_or_create(
            property=property_obj,
            fiscal_code="RSSMRA80A01H501U",
            defaults={
                "first_name": "Mario",
                "last_name": "Rossi",
                "linked_user": client,
                "ownership_percentage": Decimal("100"),
            },
        )

        partner, _ = PartnerProfile.objects.get_or_create(
            user=partner_user,
            defaults={
                "display_name": "Studio Tecnico Demo",
                "legal_name": "Studio Tecnico Demo",
                "vat_number": "IT88888888888",
                "professional_type": "Geometra",
                "license_number": "RM-DEMO-001",
                "provinces": ["RM", "LT"],
                "status": PartnerProfile.Status.ACTIVE,
                "rating": Decimal("4.80"),
                "sla_compliance_rate": Decimal("96.00"),
                "completed_assignments": 12,
            },
        )

        service = Service.objects.filter(code="visura-catastale-immobile").first()
        if service:
            PartnerService.objects.get_or_create(
                partner=partner,
                service=service,
                defaults={
                    "partner_price": Decimal("8.00"),
                    "estimated_hours": 4,
                },
            )

            order = Order.objects.filter(customer=client, property=property_obj).first()
            if not order:
                order = Order.objects.create(
                    customer=client,
                    company=company,
                    property=property_obj,
                    customer_notes="Ordine dimostrativo.",
                )
                add_service_to_order(order, service)
                transition_order(order, Order.Status.AWAITING_PAYMENT, client)

        Case.objects.get_or_create(
            property=property_obj,
            title="Verifica documentale demo",
            defaults={
                "service_type": "Dossier Casa 360",
                "status": Case.Status.OPEN,
                "assigned_to": partner_user,
                "due_date": timezone.localdate() + timezone.timedelta(days=5),
                "created_by": agency_user,
            },
        )

        self.stdout.write(self.style.SUCCESS(
            "Demo creata. Password comune: DomusOS-Demo-2026!"
        ))
        self.stdout.write("admin@demo.domusos.local")
        self.stdout.write("agenzia@demo.domusos.local")
        self.stdout.write("cliente@demo.domusos.local")
        self.stdout.write("partner@demo.domusos.local")
