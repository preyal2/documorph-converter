# 💡 Master AI Prompt Library for Document Conversion

This repository provides tested, production-grade prompts designed for Large Language Models (Gemini, ChatGPT, Claude) to handle document formatting, OCR correction, table synthesis, and automated code generation.

---

## Prompt 1: Structure Raw / Extracted PDF Text into Formatted Word

**Use Case:** When you extract raw unformatted text from a PDF or scanned document and need an AI model to structure it into a clean, hierarchical Microsoft Word format.

```markdown
You are an expert document typesetter and typography specialist. Below is raw unformatted text extracted from a PDF document:

--- BEGIN EXTRACTED TEXT ---
[PASTE YOUR RAW TEXT HERE]
--- END EXTRACTED TEXT ---

Your goal is to organize this content into a professional, human-readable Microsoft Word document format following these strict rules:

1. Document Hierarchy:
   - Identify the primary document title and assign it `# Document Title`.
   - Identify major sections and format them as `## Heading 1` and `### Heading 2`.
2. Tables & Data:
   - Where numeric data, invoice line items, or matrix values appear, convert them into Markdown tables with explicit header rows.
3. List Elements:
   - Convert disjointed bullet points into formatted `- ` lists or numbered `1. ` lists.
4. Clean OCR Artifacts:
   - Repair broken hyphenated words at line breaks (e.g. `de- velopment` -> `development`).
   - Fix corrupted currency symbols, dates, or emails.
5. Output Format:
   - Provide the complete structured document in clean GitHub Flavored Markdown ready for export into Microsoft Word (.docx).
```

---

## Prompt 2: OCR Error Correction & Table Repair

**Use Case:** When an OCR scanned PDF produces broken words, misplaced columns, or merged cells.

```markdown
Act as a forensic document restoration specialist. I have raw OCR output from a degraded or scanned PDF document:

[PASTE OCR TEXT HERE]

Execute the following corrections:
1. Reconstruct misidentified characters (e.g., 'l' vs '1', 'O' vs '0', 'rn' vs 'm').
2. Reconstruct column alignments into a Markdown table structure.
3. Preserve all original numbers, figures, and legal disclaimers without omitting any details.
4. Highlight any sections where the original text was completely illegible by tagging it with `[UNRESOLVED_TEXT]`.
```

---

## Prompt 3: Building a Standalone Python Converter Script

**Use Case:** To prompt an AI to generate a standalone Python script for offline conversions.

```markdown
Write a complete, production-ready Python script that performs two-way conversion between Word (.docx) and Adobe PDF (.pdf) files.

Requirements:
1. Libraries:
   - Use `pdf2docx` for PDF to DOCX conversion.
   - Use `docx2pdf` (with graceful fallback to `python-docx` + `reportlab`) for DOCX to PDF conversion.
2. CLI Interface:
   - Use `argparse` with two primary subcommands:
     `python convert.py word2pdf -i input.docx -o output.pdf`
     `python convert.py pdf2word -i input.pdf -o output.docx`
3. Features:
   - Progress bar using `tqdm`.
   - Verification that input files exist and output directories are created.
   - Comprehensive exception handling with informative error output.
```

---

## Prompt 4: Synthesizing Professional Resumes / Invoices

**Use Case:** Converting bullet points into an executive resume or branded business invoice.

```markdown
Act as a professional executive resume writer and document designer.
Transform the following background details into a high-impact, modern executive resume ready for Word and PDF:

[PASTE CANDIDATE DETAILS HERE]

Structure:
- Header: Name, Contact, LinkedIn, Location.
- Professional Summary (3-4 impactful sentences).
- Core Competencies (formatted as a 3-column table or clean bullet grid).
- Professional Experience (Reverse chronological, action verbs, quantified metrics).
- Education & Certifications.
- Apply consistent typography rules for headings, body text, and dates.
```
