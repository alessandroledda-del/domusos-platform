from io import BytesIO
from unittest.mock import Mock, patch
from django.test import SimpleTestCase, override_settings
from pypdf import PdfWriter
from .antivirus import MalwareDetectedError, scan_file
from .ocr import classify_document, extract_pdf_text

class OcrClassificationTest(SimpleTestCase):
    def test_classifies_cadastral_document(self):
        document_type, confidence = classify_document(
            "documento.pdf",
            "Visura catastale foglio 10 particella 22 rendita catastale",
        )
        self.assertEqual(document_type, "CADASTRAL")
        self.assertGreater(confidence, 0.5)

    def test_unknown_document_is_other(self):
        document_type, confidence = classify_document("allegato_generico.pdf")
        self.assertEqual(document_type, "OTHER")
        self.assertLess(confidence, 0.5)

    def test_extracts_empty_text_from_blank_pdf(self):
        stream = BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        writer.write(stream)
        stream.seek(0)
        text = extract_pdf_text(stream)
        self.assertEqual(text, "")

class AntivirusTest(SimpleTestCase):
    @override_settings(ANTIVIRUS_ENABLED=False)
    def test_disabled_scan(self):
        result = scan_file(BytesIO(b"test"))
        self.assertEqual(result["status"], "SKIPPED")

    @patch("apps.documents.antivirus.pyclamd.ClamdNetworkSocket")
    @override_settings(ANTIVIRUS_ENABLED=True, CLAMAV_HOST="clamav", CLAMAV_PORT=3310)
    def test_clean_file(self, socket_mock):
        socket_mock.return_value.scan_stream.return_value = None
        result = scan_file(BytesIO(b"clean"))
        self.assertEqual(result["status"], "CLEAN")

    @patch("apps.documents.antivirus.pyclamd.ClamdNetworkSocket")
    @override_settings(ANTIVIRUS_ENABLED=True, CLAMAV_HOST="clamav", CLAMAV_PORT=3310)
    def test_detected_file(self, socket_mock):
        socket_mock.return_value.scan_stream.return_value = {
            "stream": ("FOUND", "Eicar-Test-Signature")
        }
        with self.assertRaises(MalwareDetectedError):
            scan_file(BytesIO(b"infected"))
