from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import time
from typing import Dict, List
import uvicorn
from service import ModerationService
import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging with rotation
log_handler = RotatingFileHandler(
    'logs/app.log',           # Log file path
    maxBytes=1024*1024,       # 1MB per file
    backupCount=5,            # Keep 5 backup files
    encoding='utf-8'
)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

app = FastAPI(title="Content Moderation API")
moderation_service = ModerationService()

# Simple request tracking
request_times: List[float] = []

class TextRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    scores: Dict[str, float]

@app.post("/moderate", response_model=ModerationResponse)
async def moderate_text(request: TextRequest):
    # Track request time
    current_time = time.time()
    request_times.append(current_time)
    
    # Remove requests older than 1 second
    request_times[:] = [t for t in request_times if current_time - t <= 1.0]
    
    # Calculate and log requests per second
    rps = len(request_times)
    logger.info(f"Current requests per second: {rps}")
    
    try:
        # Get moderation scores
        scores = moderation_service.get_moderation_scores(request.text)
        
        return ModerationResponse(scores=scores)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 