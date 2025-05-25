from fastapi import FastAPI
from src.utils.logger import setup_app_logger
from src.moderation.controller import router as moderation_router

logger = setup_app_logger(__name__)

app = FastAPI(
    title="Text Moderation API",
    description="API for text moderation using AI models",
    version="1.0.0"
)

# Include routers
app.include_router(moderation_router, tags=["moderation"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 