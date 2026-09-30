# 📄 DocuMorph – Bidirectional Word (.docx) ⇄ PDF Document Converter

[![Developed by Preyal Modi](https://img.shields.io/badge/Developed%20by-Preyal%20Modi-6366f1?style=for-the-badge&logo=github)](https://github.com/preyal2)
[![Live Web App](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-0284c7?style=for-the-badge&logo=github)](https://preyal2.github.io/documorph-converter/)
[![CI Status](https://img.shields.io/badge/CI-Passing-10b981?style=for-the-badge&logo=githubactions)](https://github.com/preyal2/documorph-converter/actions)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-3776ab?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **Engineered & Developed with precision by [Preyal Modi](https://github.com/preyal2).**  
> **DocuMorph** is a high-fidelity bidirectional document conversion engine and REST microservice. Designed for seamless two-way conversion between **Microsoft Word (`.docx`)** and **Adobe PDF (`.pdf`)**, it features a multi-tier fault-tolerant conversion pipeline, layout & typography retention, a crisp modern white glassmorphic interface, and 100% privacy-first local processing.

🌐 **Try the Live Interactive Web App:** [https://preyal2.github.io/documorph-converter/](https://preyal2.github.io/documorph-converter/)

---

## 🌟 Key Features & Innovations

- 🔄 **Bidirectional Dual Conversion Engine**: Effortlessly convert **Word to PDF** and **PDF to Word** with automatic format sniffing and drag-and-drop support.
- 🎨 **Modern Crisp White Aesthetics**: Ultra-clean white glassmorphic interface with soft ambient lighting, micro-animations, and one-click sample document loaders.
- 🛡️ **Fault-Tolerant Multi-Tier Pipeline**:
  - *Word ➔ PDF*: Native MS Word COM Automation ➔ Headless LibreOffice ➔ Pure Python ReportLab Flowables ➔ Raw Stream Extractor.
  - *PDF ➔ Word*: AI vector layout reconstruction (`pdf2docx`) ➔ PyPDF stream extractor ➔ Emergency printable text recovery.
- 🔒 **100% Privacy & Auto-Purging**: Documents are processed locally on your machine and purged automatically after 30 minutes. Zero telemetry and zero cloud leakage.
- ⚡ **Full RESTful Microservice**: Built with FastAPI, OpenAPI Swagger UI, background garbage collection, and automated GitHub Actions CI/CD.

---

## 🗂️ Project Structure

```
documorph-converter/
├── run.py                       # One-click app launcher (starts server + opens browser)
├── requirements.txt             # Pinned cross-platform Python dependencies (UTF-8)
├── README.md                    # Master project guide & documentation
│
├── docs/                        # Dedicated Technical Documentation
│   ├── FRONTEND.md              # UI architecture, tokens, components, CSS & JS
│   ├── BACKEND.md               # FastAPI microservice endpoints, conversion engines
│   ├── ARCHITECTURE.md          # Sequence diagrams, data pipelines & privacy boundaries
│   └── PROMPTS.md               # Master AI prompt repository for document tasks
│
├── frontend/                    # Web Client (Served via GitHub Pages & FastAPI)
│   ├── index.html               # Semantic HTML5 layout with glassmorphic cards
│   ├── css/style.css            # Custom CSS3 design system (modern white primary theme)
│   └── js/app.js                # Client controller with verified Base64 sample loaders
│
├── backend/                     # High-Performance API Microservice
│   ├── app.py                   # FastAPI server & route handlers
│   ├── utils.py                 # File validation, UUID hashing & cleanup tasks
│   ├── samples/                 # Verified sample documents (DOCX & PDF)
│   └── converters/              # Conversion modules
│       ├── __init__.py
│       ├── word_to_pdf.py       # DOCX -> PDF multi-tier converter (safe COM & ReportLab)
│       └── pdf_to_word.py       # PDF -> DOCX multi-tier converter (scoped cv & raw fallback)
│
└── tests/                       # Automated Test Suite (100% Passing)
    ├── test_converters.py       # Conversion engine roundtrip tests
    └── test_api.py              # API endpoint integration tests
```

---

## 🚀 Quickstart: Running Locally

### 1. Prerequisites
* Python 3.10+ (Tested on Python 3.10, 3.11, 3.12, and 3.14 on Windows & Linux)

### 2. Installation & Setup

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

Start the application with a single command:

```bash
python run.py
```

This will automatically:
1. Initialize the FastAPI backend server on `http://127.0.0.1:8000`.
2. Open your default web browser directly to the DocuMorph Web UI.
3. Expose interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## 🧪 Automated Testing

DocuMorph includes verified test suites covering conversion integrity and REST API endpoints:

```bash
python -m unittest tests/test_converters.py
python -m unittest tests/test_api.py
```

All tests pass 100% with full roundtrip verification and valid document structures.

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
* **Live Interactive Demo:** [https://preyal2.github.io/documorph-converter/](https://preyal2.github.io/documorph-converter/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
