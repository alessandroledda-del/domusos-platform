from django.core.management.base import BaseCommand
from apps.catalog.models import Service, ServiceCategory

CATALOG = [
    {
        "code": "catasto",
        "name": "Catasto",
        "sort_order": 10,
        "services": [
            {
                "code": "visura-catastale-immobile",
                "name": "Visura catastale per immobile",
                "short_description": "Dati catastali aggiornati dell'unità immobiliare.",
                "base_price": "19.90",
                "sla_hours": 4,
                "delivery_mode": "HYBRID",
                "required_fields": ["comune", "foglio", "particella", "subalterno"],
                "is_featured": True,
            },
            {
                "code": "planimetria-catastale",
                "name": "Planimetria catastale",
                "short_description": "Planimetria depositata presso il Catasto.",
                "base_price": "34.90",
                "sla_hours": 24,
                "delivery_mode": "MANUAL",
                "required_fields": ["intestatario", "codice_fiscale", "dati_catastali"],
            },
            {
                "code": "estratto-mappa",
                "name": "Estratto di mappa",
                "short_description": "Rappresentazione cartografica della particella.",
                "base_price": "29.90",
                "sla_hours": 12,
                "delivery_mode": "HYBRID",
                "required_fields": ["comune", "foglio", "particella"],
            },
        ],
    },
    {
        "code": "conservatoria",
        "name": "Conservatoria",
        "sort_order": 20,
        "services": [
            {
                "code": "visura-ipotecaria",
                "name": "Visura ipotecaria",
                "short_description": "Verifica trascrizioni, iscrizioni e formalità.",
                "base_price": "49.90",
                "sla_hours": 24,
                "delivery_mode": "MANUAL",
                "required_fields": ["soggetto_o_immobile", "conservatoria"],
                "is_featured": True,
            },
            {
                "code": "nota-trascrizione",
                "name": "Nota di trascrizione",
                "short_description": "Recupero della nota relativa a una formalità.",
                "base_price": "39.90",
                "sla_hours": 24,
                "delivery_mode": "MANUAL",
                "required_fields": ["numero_formalita", "anno", "conservatoria"],
            },
        ],
    },
    {
        "code": "camera-commercio",
        "name": "Camera di Commercio",
        "sort_order": 30,
        "services": [
            {
                "code": "visura-camerale-ordinaria",
                "name": "Visura camerale ordinaria",
                "short_description": "Dati ufficiali e assetto attuale dell'impresa.",
                "base_price": "14.90",
                "sla_hours": 4,
                "delivery_mode": "AUTOMATIC",
                "required_fields": ["denominazione_o_partita_iva"],
                "is_featured": True,
            },
            {
                "code": "visura-camerale-storica",
                "name": "Visura camerale storica",
                "short_description": "Evoluzione storica dei dati societari.",
                "base_price": "24.90",
                "sla_hours": 8,
                "delivery_mode": "HYBRID",
                "required_fields": ["denominazione_o_partita_iva"],
            },
        ],
    },
    {
        "code": "pra",
        "name": "PRA",
        "sort_order": 40,
        "services": [
            {
                "code": "visura-targa-pra",
                "name": "Visura targa PRA",
                "short_description": "Dati giuridici e tecnici associati alla targa.",
                "base_price": "19.90",
                "sla_hours": 4,
                "delivery_mode": "AUTOMATIC",
                "required_fields": ["targa"],
                "is_featured": True,
            },
        ],
    },
    {
        "code": "dossier",
        "name": "Dossier e servizi speciali",
        "sort_order": 50,
        "services": [
            {
                "code": "dossier-casa-360",
                "name": "Dossier Casa 360°",
                "short_description": "Raccolta coordinata dei principali documenti per la compravendita.",
                "base_price": "249.00",
                "sla_hours": 120,
                "delivery_mode": "MANUAL",
                "required_fields": ["immobile", "intestatari", "finalita"],
                "is_featured": True,
            },
        ],
    },
]

class Command(BaseCommand):
    help = "Carica il catalogo servizi DomusOS iniziale."

    def handle(self, *args, **options):
        for category_data in CATALOG:
            services = category_data.pop("services")
            category, _ = ServiceCategory.objects.update_or_create(
                code=category_data["code"],
                defaults=category_data,
            )
            for service_data in services:
                Service.objects.update_or_create(
                    code=service_data["code"],
                    defaults={**service_data, "category": category},
                )
        self.stdout.write(self.style.SUCCESS("Catalogo DomusOS caricato."))
