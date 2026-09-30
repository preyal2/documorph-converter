"""
PDF to Word Converter Module.
Provides multi-tier conversion strategies:
1. pdf2docx (Advanced layout reconstruction, tables, fonts, shapes, and images).
2. pypdf + python-docx fallback (Extracts text and reconstructs pages when binary streams fail).
"""

from pathlib import Path
from docx import Document
from pypdf import PdfReader

def convert_pdf_to_docx_fallback(pdf_path: str, docx_path: str):
    """
    Fallback converter: Reads text blocks from PDF using pypdf and builds a formatted DOCX.
    """
    reader = PdfReader(pdf_path)
    doc = Document()

    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if idx > 0:
            doc.add_page_break()

        doc.add_heading(f"Page {idx + 1}", level=2)
        paragraphs = text.split("\n\n")
        for p in paragraphs:
            clean_p = p.strip()
            if clean_p:
                doc.add_paragraph(clean_p)

    doc.save(docx_path)


def convert_pdf_to_word(input_pdf: str, output_docx: str, start_page: int = 0, end_page: int = None) -> dict:
    """
    Main entry point for PDF -> DOCX conversion.
    Returns conversion metadata including engine used and file sizes.
    """
    input_path = Path(input_pdf).resolve()
    output_path = Path(output_docx).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_pdf}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    engine_used = None
    error_log = []

    # Attempt Tier 1: pdf2docx
    try:
        from pdf2docx import Converter
        cv = Converter(str(input_path))
        try:
            cv.convert(str(output_path), start=start_page, end=end_page)
            if output_path.exists() and output_path.stat().st_size > 0:
                engine_used = "pdf2docx-ai-layout"
        finally:
            cv.close()
    except Exception as e:
        error_log.append(f"pdf2docx failed: {str(e)}")

    # Attempt Tier 2: pypdf fallback
    if not engine_used:
        try:
            convert_pdf_to_docx_fallback(str(input_path), str(output_path))
            if output_path.exists() and output_path.stat().st_size > 0:
                engine_used = "pypdf-text-fallback"
        except Exception as e:
            error_log.append(f"pypdf fallback failed: {str(e)}")
            raise RuntimeError(f"All PDF-to-Word conversions failed: {'; '.join(error_log)}")

    return {
        "status": "success",
        "engine": engine_used,
        "input_size_bytes": input_path.stat().st_size,
        "output_size_bytes": output_path.stat().st_size,
        "warnings": error_log if error_log else None
    }
