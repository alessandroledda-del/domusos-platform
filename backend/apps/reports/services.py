from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import PropertyReport

def build_property_snapshot(property_obj):
    return {
        "property_id": property_obj.id,
        "title": property_obj.title,
        "address": property_obj.address,
        "municipality": property_obj.municipality,
        "province": property_obj.province,
        "status": property_obj.status,
        "domus_score": property_obj.domus_score,
        "owners": [
            {
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "ownership_percentage": str(owner.ownership_percentage),
            }
            for owner in property_obj.owners.all()
        ],
        "documents": [
            {
                "name": document.name,
                "document_type": document.document_type,
                "status": document.status,
            }
            for document in property_obj.documents.all()
        ],
    }

def generate_property_report(property_obj, user):
    snapshot = build_property_snapshot(property_obj)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 60
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "DomusOS Property Report")
    y -= 36

    pdf.setFont("Helvetica", 11)
    lines = [
        f"Immobile: {snapshot['title']}",
        f"Indirizzo: {snapshot['address']}, {snapshot['municipality']} ({snapshot['province']})",
        f"Stato: {snapshot['status']}",
        f"Domus Score: {snapshot['domus_score']}/100",
        "",
        "Documenti:",
    ]
    for item in snapshot["documents"]:
        lines.append(f"- {item['name']} [{item['document_type']}] - {item['status']}")

    for line in lines:
        pdf.drawString(50, y, line[:110])
        y -= 18
        if y < 60:
            pdf.showPage()
            y = height - 60

    pdf.save()
    buffer.seek(0)

    report = PropertyReport.objects.create(
        property=property_obj,
        created_by=user,
        title=f"Report {property_obj.title}",
        snapshot=snapshot,
    )
    report.file.save(
        f"property-{property_obj.id}-report.pdf",
        ContentFile(buffer.read()),
        save=True,
    )
    return report
