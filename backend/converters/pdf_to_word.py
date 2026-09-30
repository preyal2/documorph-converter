"""
PDF to Word Converter Module.
Provides robust multi-tier conversion strategies:
1. pdf2docx (Advanced vector layout reconstruction, tables, fonts, shapes).
2. pypdf + python-docx fallback (Extracts text and reconstructs pages when binary layout fails).
3. Raw stream extractor (Emergency fallback for partially corrupted or encrypted PDFs).
"""

import re
from pathlib import Path
from docx import Document
from pypdf import PdfReader

def convert_pdf_to_docx_fallback(pdf_path: str, docx_path: str):
    """
    Fallback converter: Reads text blocks from PDF using pypdf and builds a formatted DOCX.
    """
    reader = PdfReader(pdf_path)
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            pass

    doc = Document()
    doc.add_heading("Extracted Document Content", level=0)

    has_content = False
    for idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""

        if text.strip():
            has_content = True
            if idx > 0:
                doc.add_page_break()

            doc.add_heading(f"Page {idx + 1}", level=2)
            paragraphs = text.split("\n\n")
            for p in paragraphs:
                clean_p = p.strip()
                if clean_p:
                    doc.add_paragraph(clean_p)

    if not has_content:
        doc.add_paragraph("[Scanned or empty PDF content. No text layers detected.]")

    doc.save(docx_path)


def convert_raw_pdf_fallback(pdf_path: str, docx_path: str):
    """
    Emergency Tier 3: Extracts ASCII/Unicode printable text streams from corrupted PDF files
    and wraps them into a valid DOCX document that Word can open cleanly.
    """
    doc = Document()
    doc.add_heading("Recovered Document Content", level=0)

    try:
        with open(pdf_path, "rb") as f:
            raw_bytes = f.read()
        
        # Extract printable text sequences
        text_matches = re.findall(rb'[\x20-\x7E\t\n\r]{4,}', raw_bytes)
        recovered_lines = []
        for match in text_matches:
            try:
                line = match.decode('utf-8', errors='ignore').strip()
                if line and not line.startswith(('%', 'obj', 'endobj', 'stream', 'endstream')):
                    recovered_lines.append(line)
            except Exception:
                pass

        if recovered_lines:
            for line in recovered_lines[:500]:
                doc.add_paragraph(line)
        else:
            doc.add_paragraph("Document stream could not be decoded.")
    except Exception as e:
        doc.add_paragraph(f"Notice: Document recovered with basic content wrapper ({str(e)}).")

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
    cv = None
    try:
        from pdf2docx import Converter
        cv = Converter(str(input_path))
        cv.convert(str(output_path), start=start_page, end=end_page)
        if output_path.exists() and output_path.stat().st_size > 0:
            engine_used = "pdf2docx-ai-layout"
    except Exception as e:
        error_log.append(f"pdf2docx layout engine failed: {str(e)}")
    finally:
        if cv is not None:
            try:
                cv.close()
            except Exception:
                pass

    # Attempt Tier 2: pypdf fallback
    if not engine_used:
        try:
            convert_pdf_to_docx_fallback(str(input_path), str(output_path))
            if output_path.exists() and output_path.stat().st_size > 0:
                engine_used = "pypdf-text-fallback"
        except Exception as e:
            error_log.append(f"pypdf fallback failed: {str(e)}")

    # Attempt Tier 3: Raw stream extraction
    if not engine_used:
        try:
            convert_raw_pdf_fallback(str(input_path), str(output_path))
            if output_path.exists() and output_path.stat().st_size > 0:
                engine_used = "raw-stream-fallback"
        except Exception as e:
            error_log.append(f"emergency fallback failed: {str(e)}")
            raise RuntimeError(f"All conversion methods failed: {'; '.join(error_log)}")

    return {
        "status": "success",
        "engine": engine_used,
        "input_size_bytes": input_path.stat().st_size,
        "output_size_bytes": output_path.stat().st_size,
        "warnings": error_log if error_log else None
    }
