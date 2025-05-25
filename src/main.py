from fastapi import FastAPI
from src.utils.logger import setup_app_logger
from src.moderation.controller import router as moderation_router

logger = setup_app_logger(__name__)

app = FastAPI(title="Text Moderation API")

# Include routers
app.include_router(moderation_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 