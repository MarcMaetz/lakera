from fastapi import FastAPI
from src.utils.logger import setup_app_logger
from src.moderation.controller import router as moderation_router

# Configure logging
logger = setup_app_logger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Text Moderation API",
        description="API for text moderation using AI models",
        version="1.0.0",
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