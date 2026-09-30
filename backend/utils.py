"""
Utility functions for file management, validation, and scheduled cleanup.
"""

import os
import time
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
OUTPUT_DIR = STORAGE_DIR / "outputs"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_DOCX_EXTENSIONS = {".docx", ".doc"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}

def validate_extension(filename: str, target_type: str) -> bool:
    ext = Path(filename).suffix.lower()
    if target_type == "docx":
        return ext in ALLOWED_DOCX_EXTENSIONS
    elif target_type == "pdf":
        return ext in ALLOWED_PDF_EXTENSIONS
    return False

def generate_session_paths(original_filename: str, output_ext: str) -> tuple[Path, Path, str]:
    """
    Generates unique isolated filepaths for upload and output.
    Returns (upload_path, output_path, unique_id)
    """
    clean_stem = Path(original_filename).stem.replace(" ", "_")
    unique_id = uuid.uuid4().hex[:10]
    upload_ext = Path(original_filename).suffix.lower()
    
    upload_filename = f"{clean_stem}_{unique_id}{upload_ext}"
    output_filename = f"{clean_stem}_{unique_id}{output_ext}"
    
    upload_path = UPLOAD_DIR / upload_filename
    output_path = OUTPUT_DIR / output_filename
    
    return upload_path, output_path, unique_id

def cleanup_stale_files(max_age_seconds: int = 1800):
    """
    Removes temporary files older than max_age_seconds (default: 30 minutes).
    Ensures privacy and prevents disk storage bloat.
    """
    now = time.time()
    for directory in [UPLOAD_DIR, OUTPUT_DIR]:
        if directory.exists():
            for item in directory.glob("*"):
                if item.is_file():
                    try:
                        if now - item.stat().st_mtime > max_age_seconds:
                            item.unlink()
                    except Exception:
                        pass

def format_file_size(size_in_bytes: int) -> str:
    """Format bytes into readable string (e.g. 1.2 MB)."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} TB"
