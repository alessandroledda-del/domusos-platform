from dataclasses import dataclass
from decimal import Decimal

@dataclass
class RuleResult:
    code: str
    title: str
    passed: bool
    severity: str
    description: str
    evidence: dict
    weight: int

class BaseRule:
    code = "BASE"
    title = "Regola base"
    severity = "LOW"
    weight = 10

    def evaluate(self, property_obj):
        raise NotImplementedError

class CadastralIdentityRule(BaseRule):
    code = "CADASTRAL_IDENTITY_COMPLETE"
    title = "Identificazione catastale completa"
    severity = "HIGH"
    weight = 15

    def evaluate(self, property_obj):
        fields = {
            "foglio": property_obj.cadastral_sheet,
            "particella": property_obj.cadastral_particle,
            "subalterno": property_obj.cadastral_subaltern,
        }
        missing = [name for name, value in fields.items() if not value]
        return RuleResult(
            code=self.code,
            title=self.title,
            passed=not missing,
            severity=self.severity,
            description=(
                "I dati catastali essenziali risultano presenti."
                if not missing
                else f"Mancano i seguenti dati catastali: {', '.join(missing)}."
            ),
            evidence={"fields": fields, "missing": missing},
            weight=self.weight,
        )

class OwnershipQuotaRule(BaseRule):
    code = "OWNERSHIP_QUOTAS_100"
    title = "Quote proprietarie coerenti"
    severity = "HIGH"
    weight = 15

    def evaluate(self, property_obj):
        owners = list(property_obj.owners.all())
        total = sum((owner.ownership_percentage for owner in owners), Decimal("0"))
        passed = bool(owners) and total == Decimal("100")
        return RuleResult(
            code=self.code,
            title=self.title,
            passed=passed,
            severity=self.severity,
            description=(
                "Le quote proprietarie sommano al 100%."
                if passed
                else f"Le quote proprietarie rilevate sommano a {total}%."
            ),
            evidence={"owners_count": len(owners), "total_percentage": str(total)},
            weight=self.weight,
        )

class DeedDocumentRule(BaseRule):
    code = "DEED_PRESENT"
    title = "Atto di provenienza presente"
    severity = "HIGH"
    weight = 15

    def evaluate(self, property_obj):
        documents = property_obj.documents.filter(document_type="DEED")
        passed = documents.exists()
        return RuleResult(
            code=self.code,
            title=self.title,
            passed=passed,
            severity=self.severity,
            description=(
                "È presente almeno un atto di provenienza."
                if passed
                else "Non risulta caricato un atto di provenienza."
            ),
            evidence={"document_ids": list(documents.values_list("id", flat=True))},
            weight=self.weight,
        )

class CadastralDocumentRule(BaseRule):
    code = "CADASTRAL_DOCS_PRESENT"
    title = "Documentazione catastale presente"
    severity = "MEDIUM"
    weight = 10

    def evaluate(self, property_obj):
        required = {"CADASTRAL", "PLAN"}
        present = set(property_obj.documents.values_list("document_type", flat=True))
        missing = sorted(required - present)
        return RuleResult(
            code=self.code,
            title=self.title,
            passed=not missing,
            severity=self.severity,
            description=(
                "Visura e planimetria risultano presenti."
                if not missing
                else f"Documenti catastali mancanti: {', '.join(missing)}."
            ),
            evidence={"present": sorted(present), "missing": missing},
            weight=self.weight,
        )

class EnergyCertificateRule(BaseRule):
    code = "ENERGY_CERTIFICATE_PRESENT"
    title = "Attestato di prestazione energetica presente"
    severity = "MEDIUM"
    weight = 10

    def evaluate(self, property_obj):
        documents = property_obj.documents.filter(document_type="ENERGY")
        passed = documents.exists()
        return RuleResult(
            code=self.code,
            title=self.title,
            passed=passed,
            severity=self.severity,
            description=(
                "È presente un documento APE."
                if passed
                else "Non risulta caricato un attestato di prestazione energetica."
            ),
            evidence={"document_ids": list(documents.values_list("id", flat=True))},
            weight=self.weight,
        )

class MortgageSearchRule(BaseRule):
    code = "MORTGAGE_SEARCH_PRESENT"
    title = "Verifica ipotecaria presente"
    severity = "HIGH"
    weight = 15

    def evaluate(self, property_obj):
        documents = property_obj.documents.filter(document_type="MORTGAGE")
        passed = documents.exists()
        return RuleResult(
            code=self.code,
            title=self.title,
            passed=passed,
            severity=self.severity,
            description=(
                "È presente una visura ipotecaria."
                if passed
                else "Non risulta caricata una visura ipotecaria."
            ),
            evidence={"document_ids": list(documents.values_list("id", flat=True))},
            weight=self.weight,
        )

class DocumentProcessingRule(BaseRule):
    code = "DOCUMENTS_PROCESSED"
    title = "Documenti elaborati senza errori"
    severity = "MEDIUM"
    weight = 10

    def evaluate(self, property_obj):
        failed = property_obj.documents.filter(status="FAILED")
        queued = property_obj.documents.filter(status__in=["QUEUED", "PROCESSING"])
        passed = not failed.exists() and not queued.exists()
        return RuleResult(
            code=self.code,
            title=self.title,
            passed=passed,
            severity=self.severity,
            description=(
                "I documenti non presentano errori o elaborazioni pendenti."
                if passed
                else "Sono presenti documenti falliti o ancora in elaborazione."
            ),
            evidence={
                "failed_ids": list(failed.values_list("id", flat=True)),
                "pending_ids": list(queued.values_list("id", flat=True)),
            },
            weight=self.weight,
        )

class OpenCriticalFindingsRule(BaseRule):
    code = "NO_PREVIOUS_CRITICAL_FINDINGS"
    title = "Assenza di criticità pregresse aperte"
    severity = "CRITICAL"
    weight = 10

    def evaluate(self, property_obj):
        critical = property_obj.compliance_findings.filter(
            severity="CRITICAL",
            status__in=["OPEN", "ACKNOWLEDGED"],
        )
        passed = not critical.exists()
        return RuleResult(
            code=self.code,
            title=self.title,
            passed=passed,
            severity=self.severity,
            description=(
                "Non risultano criticità pregresse aperte."
                if passed
                else "Sono presenti criticità pregresse ancora aperte."
            ),
            evidence={"finding_ids": list(critical.values_list("id", flat=True))},
            weight=self.weight,
        )

DEFAULT_RULES = [
    CadastralIdentityRule(),
    OwnershipQuotaRule(),
    DeedDocumentRule(),
    CadastralDocumentRule(),
    EnergyCertificateRule(),
    MortgageSearchRule(),
    DocumentProcessingRule(),
    OpenCriticalFindingsRule(),
]
