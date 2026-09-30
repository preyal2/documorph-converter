"""
Unit and Integration Tests for DocuMorph Converters & API Endpoints.
"""

import sys
import unittest
from pathlib import Path
from docx import Document
from pypdf import PdfReader

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.converters.word_to_pdf import convert_word_to_pdf
from backend.converters.pdf_to_word import convert_pdf_to_word

class TestDocuMorphConverters(unittest.TestCase):

    def setUp(self):
        self.test_dir = PROJECT_ROOT / "tests" / "fixtures"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.sample_docx = self.test_dir / "sample_test.docx"
        self.sample_pdf = self.test_dir / "sample_test.pdf"
        self.roundtrip_docx = self.test_dir / "roundtrip_test.docx"

        # Generate a sample docx for testing
        doc = Document()
        doc.add_heading("DocuMorph Test Document", level=0)
        doc.add_paragraph("This is a synthesized test paragraph containing formatted text.")
        
        table = doc.add_table(rows=2, cols=2)
        table.cell(0, 0).text = "Header A"
        table.cell(0, 1).text = "Header B"
        table.cell(1, 0).text = "Value 1"
        table.cell(1, 1).text = "Value 2"

        doc.save(str(self.sample_docx))

    def tearDown(self):
        # Clean up fixture files
        for f in [self.sample_docx, self.sample_pdf, self.roundtrip_docx]:
            if f.exists():
                try:
                    f.unlink()
                except Exception:
                    pass

    def test_word_to_pdf_conversion(self):
        """Test Word (.docx) to PDF conversion."""
        result = convert_word_to_pdf(str(self.sample_docx), str(self.sample_pdf))
        self.assertEqual(result["status"], "success")
        self.assertTrue(self.sample_pdf.exists())
        self.assertGreater(self.sample_pdf.stat().st_size, 0)

        # Verify PDF validity with pypdf
        reader = PdfReader(str(self.sample_pdf))
        self.assertGreaterEqual(len(reader.pages), 1)

    def test_pdf_to_word_conversion(self):
        """Test PDF to Word (.docx) roundtrip conversion."""
        # First generate PDF
        convert_word_to_pdf(str(self.sample_docx), str(self.sample_pdf))
        self.assertTrue(self.sample_pdf.exists())

        # Now convert back to DOCX
        result = convert_pdf_to_word(str(self.sample_pdf), str(self.roundtrip_docx))
        self.assertEqual(result["status"], "success")
        self.assertTrue(self.roundtrip_docx.exists())
        self.assertGreater(self.roundtrip_docx.stat().st_size, 0)

        # Verify generated DOCX can be opened
        doc = Document(str(self.roundtrip_docx))
        self.assertTrue(len(doc.paragraphs) > 0 or len(doc.tables) > 0)

if __name__ == "__main__":
    unittest.main()
