"""
DocuMorph Core Backend API.
Built with FastAPI. Supports bidirectional Word <-> PDF conversions,
file metadata extraction, health monitoring, and static asset serving.
"""

import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.converters.word_to_pdf import convert_word_to_pdf
from backend.converters.pdf_to_word import convert_pdf_to_word
from backend.utils import (
    UPLOAD_DIR,
    OUTPUT_DIR,
    validate_extension,
    generate_session_paths,
    cleanup_stale_files,
    format_file_size
)

app = FastAPI(
    title="DocuMorph Document Converter API",
    description="High-performance Word ⇄ PDF bidirectional conversion microservice.",
    version="1.0.0"
)

# Enable CORS for local development and embedded widgets
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

@app.on_event("startup")
async def startup_event():
    cleanup_stale_files(max_age_seconds=600)

@app.get("/api/health")
async def health_check():
    """System diagnostic and health monitor."""
    return {
        "status": "healthy",
        "service": "DocuMorph Converter",
        "version": "1.0.0",
        "capabilities": {
            "word_to_pdf": True,
            "pdf_to_word": True,
            "batch_conversion": True
        }
    }

@app.post("/api/convert/word-to-pdf")
async def api_word_to_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Convert Word (.docx, .doc) to PDF.
    """
    if not validate_extension(file.filename, "docx"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format: '{file.filename}'. Please upload a .docx or .doc file."
        )

    upload_path, output_path, session_id = generate_session_paths(file.filename, ".pdf")

    try:
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run conversion
        result = convert_word_to_pdf(str(upload_path), str(output_path))

        background_tasks.add_task(cleanup_stale_files, 1800)

        return {
            "status": "success",
            "session_id": session_id,
            "original_filename": file.filename,
            "output_filename": output_path.name,
            "download_url": f"/api/download/{output_path.name}",
            "engine": result.get("engine"),
            "original_size": format_file_size(result.get("input_size_bytes", 0)),
            "converted_size": format_file_size(result.get("output_size_bytes", 0)),
            "warnings": result.get("warnings")
        }
    except Exception as e:
        if upload_path.exists():
            upload_path.unlink()
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")


@app.post("/api/convert/pdf-to-word")
async def api_pdf_to_word(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Convert PDF (.pdf) to Word (.docx).
    """
    if not validate_extension(file.filename, "pdf"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format: '{file.filename}'. Please upload a valid .pdf file."
        )

    upload_path, output_path, session_id = generate_session_paths(file.filename, ".docx")

    try:
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run conversion
        result = convert_pdf_to_word(str(upload_path), str(output_path))

        background_tasks.add_task(cleanup_stale_files, 1800)

        return {
            "status": "success",
            "session_id": session_id,
            "original_filename": file.filename,
            "output_filename": output_path.name,
            "download_url": f"/api/download/{output_path.name}",
            "engine": result.get("engine"),
            "original_size": format_file_size(result.get("input_size_bytes", 0)),
            "converted_size": format_file_size(result.get("output_size_bytes", 0)),
            "warnings": result.get("warnings")
        }
    except Exception as e:
        if upload_path.exists():
            upload_path.unlink()
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """
    Secure file download endpoint.
    """
    safe_filename = Path(filename).name
    file_path = OUTPUT_DIR / safe_filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Requested file was not found or has expired.")

    # Determine media type
    media_type = "application/pdf" if file_path.suffix.lower() == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return FileResponse(
        path=str(file_path),
        filename=safe_filename,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'}
    )

# Mount frontend static directory if exists
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
