# 📄 DocuMorph - Word ⇄ PDF Bidirectional Converter

[![Developed by Preyal Modi](https://img.shields.io/badge/Developed%20by-Preyal%20Modi-6366f1?style=for-the-badge&logo=github)](https://github.com/preyal2)
[![Live Demo: GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-06b6d4?style=for-the-badge&logo=github)](https://preyal2.github.io/documorph-converter/)
[![CI Status](https://img.shields.io/badge/CI-Passing-10b981?style=for-the-badge&logo=githubactions)](https://github.com/preyal2/documorph-converter/actions)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-3776ab?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **Engineered & Developed by [Preyal Modi](https://github.com/preyal2).**  
> **DocuMorph** is an ultra-fast, high-fidelity bidirectional document conversion platform and REST microservice designed to seamlessly transform files between Microsoft Word (`.docx`) and Adobe PDF (`.pdf`). Built with a multi-tier fallback architecture, layout & typography retention, and a privacy-first local processing engine.

🌐 **Interactive Live Web Demo:** [https://preyal2.github.io/documorph-converter/](https://preyal2.github.io/documorph-converter/)

---

## 🌟 Key Highlights

- 🔄 **Bidirectional Dual Conversion Engine**: Convert **Word to PDF** and **PDF to Word** with automatic format sniffing and drag-and-drop.
- 🎨 **Modern Glassmorphic UI**: Ultra-sleek design with dark/light themes, subtle ambient lighting, micro-animations, and one-click sample document loaders.
- 🛡️ **Fault-Tolerant Multi-Tier Pipeline**:
  - *DOCX ➔ PDF*: Native MS Word COM Automation ➔ Headless LibreOffice ➔ Pure Python ReportLab Flowables.
  - *PDF ➔ DOCX*: AI vector layout reconstruction (`pdf2docx`) ➔ PyPDF stream extractor.
- 🔒 **100% Privacy & Auto-Purging**: Documents remain on your local machine and are purged automatically after 30 minutes. Zero external cloud dependencies.
- ⚡ **Full RESTful Microservice**: Built with FastAPI, OpenAPI Swagger UI, background garbage collection, and automated CI test suites.

---

## 🗂️ Project Structure

```
documorph-converter/
├── run.py                       # One-click app launcher (starts server + opens browser)
├── requirements.txt             # Pinned Python dependencies (UTF-8, cross-platform)
├── README.md                    # Master project guide & quickstart
│
├── docs/                        # Dedicated Technical Documentation
│   ├── FRONTEND.md              # UI/UX design tokens, HTML components, CSS & JS
│   ├── BACKEND.md               # Backend API specifications, engines & storage
│   ├── ARCHITECTURE.md          # Flowcharts, sequence diagrams & privacy model
│   └── PROMPTS.md               # Master AI prompt repository for document tasks
│
├── frontend/                    # Web Client (Deployed to GitHub Pages)
│   ├── index.html               # Semantic HTML5 layout & ARIA accessible controls
│   ├── css/
│   │   └── style.css            # Custom CSS3 design system, themes & animations
│   └── js/
│       └── app.js               # Client controller, drag-and-drop & API integration
│
├── backend/                     # API Microservice
│   ├── __init__.py
│   ├── app.py                   # FastAPI server & route handlers
│   ├── utils.py                 # File validation, UUID hashing & cleanup tasks
│   └── converters/              # Conversion modules
│       ├── __init__.py
│       ├── word_to_pdf.py       # DOCX -> PDF multi-tier converter
│       └── pdf_to_word.py       # PDF -> DOCX multi-tier converter
│
└── tests/                       # Automated Test Suite
    ├── test_converters.py       # Full roundtrip unit tests
    └── test_api.py              # API endpoint integration tests
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.10, 3.11, 3.12, and 3.14 on Windows & Linux)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/preyal2/documorph-converter.git
cd documorph-converter

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # On Windows
# source .venv/bin/activate # On Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Application

Run the one-click launcher from the project directory:

```bash
python run.py
```

This will automatically:
1. Initialize the FastAPI backend server on `http://127.0.0.1:8000`.
2. Open your default web browser directly to the DocuMorph Web UI.
3. Expose interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## 🧪 Automated Testing

DocuMorph includes a comprehensive test suite covering conversion integrity and REST API endpoints:

```bash
python -m unittest tests/test_converters.py
python -m unittest tests/test_api.py
```

Both test suites pass 100% with full roundtrip verification.

---

## 📚 Dedicated Technical Documentation

Each subsystem is thoroughly documented in its own dedicated document:

* 🎨 **[Frontend Documentation](docs/FRONTEND.md)**: Design system tokens, HTML structure, CSS glassmorphism, and JavaScript state machine.
* ⚙️ **[Backend Documentation](docs/BACKEND.md)**: API routes, payload formats, conversion tiers, and storage security.
* 🏛️ **[System Architecture](docs/ARCHITECTURE.md)**: Sequence diagrams, data pipelines, failure mitigation, and containerization.
* 💡 **[AI Prompt Library](docs/PROMPTS.md)**: Curated prompts for OCR correction, layout styling, and code generation.

---

## 👨‍💻 Developer & Author

**Preyal Modi**
* **GitHub Profile:** [@preyal2](https://github.com/preyal2)
* **Project Repository:** [documorph-converter](https://github.com/preyal2/documorph-converter)
* **Live Demo:** [https://preyal2.github.io/documorph-converter/](https://preyal2.github.io/documorph-converter/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
