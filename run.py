#!/usr/bin/env python3
import os
import sys
import uvicorn
from fastapi import FastAPI
from src.utils.logger import setup_app_logger
from src.moderation.controller import router as moderation_router
from src.config import API_TITLE, API_DESCRIPTION, API_VERSION

# Configure environment
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

# Configure logging
logger = setup_app_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(moderation_router)

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        reload_dirs=[project_root]
    ) 