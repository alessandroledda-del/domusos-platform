import re
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import pytesseract

DOCUMENT_HINTS = {
    "DEED": ["atto", "rogito", "notaio", "compravendita"],
    "CADASTRAL": ["visura catastale", "catasto", "foglio", "particella", "rendita"],
    "PLAN": ["planimetria", "scala", "subalterno"],
    "ENERGY": ["ape", "prestazione energetica", "classe energetica"],
    "BUILDING": ["permesso di costruire", "concessione edilizia", "scia", "cil"],
    "MORTGAGE": ["ipoteca", "conservatoria", "iscrizione", "trascrizione"],
}

def extract_pdf_text(file_obj, max_pages=20):
    file_obj.seek(0)
    reader = PdfReader(file_obj)
    chunks = []
    for page in reader.pages[:max_pages]:
        chunks.append(page.extract_text() or "")
    file_obj.seek(0)
    return "\n".join(chunks).strip()

def extract_image_text(file_obj):
    file_obj.seek(0)
    image = Image.open(file_obj)
    text = pytesseract.image_to_string(image, lang="ita+eng")
    file_obj.seek(0)
    return text.strip()

def classify_document(filename: str, extracted_text: str = ""):
    haystack = f"{filename} {extracted_text}".lower()
    scores = {}
    for document_type, hints in DOCUMENT_HINTS.items():
        scores[document_type] = sum(1 for hint in hints if hint in haystack)

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    if best_score == 0:
        return "OTHER", 0.30

    confidence = min(0.55 + best_score * 0.10, 0.95)
    return best_type, confidence

def extract_metadata(document):
    filename = Path(document.file.name).name
    suffix = Path(filename).suffix.lower()
    extracted_text = ""
    extraction_method = "filename-analysis"

    with document.file.open("rb") as file_obj:
        if suffix == ".pdf":
            extracted_text = extract_pdf_text(file_obj)
            extraction_method = "pypdf"
        elif suffix in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
            extracted_text = extract_image_text(file_obj)
            extraction_method = "tesseract"

    document_type, confidence = classify_document(filename, extracted_text)
    possible_numbers = re.findall(r"\b\d{1,8}\b", extracted_text or filename)

    return {
        "filename": filename,
        "suggested_document_type": document_type,
        "confidence": confidence,
        "possible_numbers": possible_numbers[:25],
        "text_preview": extracted_text[:3000],
        "text_length": len(extracted_text),
        "engine": "domus-document-engine-v0.7",
        "extraction_method": extraction_method,
    }
