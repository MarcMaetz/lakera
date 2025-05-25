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

class RequestTracker:
    def __init__(self):
        self.windows = {
            '1s': [],    # Last second
            '1m': [],    # Last minute
            '1h': []     # Last hour
        }
    
    def add_request(self):
        current_time = time.time()
        for window, times in self.windows.items():
            times.append(current_time)
            # Remove old requests based on window size
            if window == '1s':
                times[:] = [t for t in times if current_time - t <= 1.0]
            elif window == '1m':
                times[:] = [t for t in times if current_time - t <= 60.0]
            elif window == '1h':
                times[:] = [t for t in times if current_time - t <= 3600.0]
    
    def get_stats(self):
        return {
            '1s': len(self.windows['1s']),
            '1m': len(self.windows['1m']),
            '1h': len(self.windows['1h'])
        }

app = FastAPI(title="Content Moderation API")
moderation_service = ModerationService()
request_tracker = RequestTracker()

class TextRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    scores: Dict[str, float]

@app.post("/moderate", response_model=ModerationResponse)
async def moderate_text(request: TextRequest):
    # Track request
    request_tracker.add_request()
    
    # Log request rates
    stats = request_tracker.get_stats()
    logger.info(f"Request rates - 1s: {stats['1s']}, 1m: {stats['1m']}, 1h: {stats['1h']}")
    
    try:
        # Get moderation scores
        scores = moderation_service.get_moderation_scores(request.text)
        
        return ModerationResponse(scores=scores)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 