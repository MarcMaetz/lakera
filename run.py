#!/usr/bin/env python3
import os
import sys
import uvicorn
from typing import Optional

def setup_environment():
    """Configure the Python environment for development"""
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

    # Prevent Python from writing .pyc files
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

def run_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = True,
    log_level: str = "info"
):
    """Run the development server with the specified configuration"""
    setup_environment()
    
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        reload_dirs=[os.path.dirname(os.path.abspath(__file__))]
    )

if __name__ == "__main__":
    run_server() 