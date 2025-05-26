from fastapi import FastAPI
from src.utils.logger import setup_app_logger
from src.moderation.controller import router as moderation_router
from src.config import API_TITLE, API_DESCRIPTION, API_VERSION

# Configure logging
logger = setup_app_logger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Include routers
    app.include_router(moderation_router, tags=["moderation"])

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

# Create the application instance
app = create_app() 