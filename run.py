"""
DocuMorph One-Click Server Launcher
Starts the FastAPI application and opens the web application in your default browser.
"""

import sys
import webbrowser
import threading
import time
import uvicorn

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("=" * 60)
    print(" 🚀 Starting DocuMorph - Document Converter Microservice")
    print(" 📍 Web App: http://127.0.0.1:8000")
    print(" 📖 API Docs: http://127.0.0.1:8000/docs")
    print("=" * 60)
    
    # Auto-open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Run uvicorn server
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False)
