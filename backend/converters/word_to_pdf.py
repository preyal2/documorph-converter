"""
Word to PDF Converter Module.
Provides multi-tier conversion strategies:
1. Native MS Word COM automation via docx2pdf (Highest fidelity on Windows).
2. LibreOffice headless conversion (Cross-platform server standard).
3. Pure Python fallback via python-docx + ReportLab (Guaranteed zero-dependency fallback).
4. Raw document fallback (for corrupted docx files or plain text containers).
"""

import os
import shutil
import subprocess
import zipfile
import re
from pathlib import Path
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def convert_docx_to_pdf_reportlab(docx_path: str, pdf_path: str):
    """
    Fallback converter: Parses docx elements and builds a PDF using ReportLab.
    Ensures conversions succeed even without MS Word or LibreOffice.
    """
    pdf_doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    story = []

    # Attempt to open as valid Word docx
    try:
        doc = Document(docx_path)
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if not text:
                story.append(Spacer(1, 6))
                continue

            p_style = body_style
            if paragraph.style.name.startswith('Heading 1') or paragraph.style.name == 'Title':
                p_style = title_style if paragraph.style.name == 'Title' else h1_style
            elif paragraph.style.name.startswith('Heading'):
                p_style = h1_style

            clean_text = (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

            story.append(Paragraph(clean_text, p_style))

        # Process tables if any
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    clean_cell = cell.text.strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    row_data.append(Paragraph(clean_cell, body_style))
                table_data.append(row_data)

            if table_data:
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ]))
                story.append(Spacer(1, 10))
                story.append(t)
                story.append(Spacer(1, 10))

    except Exception:
        # Fallback for damaged or non-standard docx: extract readable text lines
        try:
            with open(docx_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_text = f.read()
            clean_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
            for line in clean_lines[:300]:
                safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(safe_line, body_style))
        except Exception:
            story.append(Paragraph("Document could not be parsed as standard Word document.", body_style))

    if not story:
        story.append(Paragraph("[Empty Document]", body_style))

    pdf_doc.build(story)


def convert_word_to_pdf(input_docx: str, output_pdf: str) -> dict:
    """
    Main entry point for DOCX -> PDF conversion.
    Returns conversion metadata including engine used and file sizes.
    """
    input_path = Path(input_docx).resolve()
    output_path = Path(output_pdf).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_docx}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    engine_used = None
    error_log = []

    # Attempt Tier 1: docx2pdf (MS Word COM on Windows)
    try:
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except Exception:
            pass

        try:
            from docx2pdf import convert
            convert(str(input_path), str(output_path))
            if output_path.exists() and output_path.stat().st_size > 0:
                engine_used = "ms-word-com"
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass
    except Exception as e:
        error_log.append(f"docx2pdf failed: {str(e)}")

    # Attempt Tier 2: LibreOffice headless if installed
    if not engine_used:
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if soffice:
            try:
                cmd = [
                    soffice,
                    "--headless",
                    "--convert-to", "pdf",
                    "--outdir", str(output_path.parent),
                    str(input_path)
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                expected_pdf = output_path.parent / (input_path.stem + ".pdf")
                if expected_pdf.exists() and expected_pdf != output_path:
                    shutil.move(str(expected_pdf), str(output_path))
                if output_path.exists() and output_path.stat().st_size > 0:
                    engine_used = "libreoffice-headless"
            except Exception as e:
                error_log.append(f"LibreOffice failed: {str(e)}")

    # Attempt Tier 3: Pure Python fallback (ReportLab)
    if not engine_used:
        try:
            convert_docx_to_pdf_reportlab(str(input_path), str(output_path))
            if output_path.exists() and output_path.stat().st_size > 0:
                engine_used = "python-reportlab-fallback"
        except Exception as e:
            error_log.append(f"ReportLab fallback failed: {str(e)}")
            raise RuntimeError(f"All conversion methods failed: {'; '.join(error_log)}")

    return {
        "status": "success",
        "engine": engine_used,
        "input_size_bytes": input_path.stat().st_size,
        "output_size_bytes": output_path.stat().st_size,
        "warnings": error_log if error_log else None
    }
