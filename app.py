from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import time
from typing import Dict, List
import uvicorn
from service import ModerationService

app = FastAPI(title="Content Moderation API")
moderation_service = ModerationService()

# Simple request tracking
request_times: List[float] = []

class TextRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    scores: Dict[str, float]
    requests_per_second: float

@app.post("/moderate", response_model=ModerationResponse)
async def moderate_text(request: TextRequest):
    # Track request time
    current_time = time.time()
    request_times.append(current_time)
    
    # Remove requests older than 1 second
    request_times[:] = [t for t in request_times if current_time - t <= 1.0]
    
    # Calculate requests per second
    rps = len(request_times)
    
    try:
        # Get moderation scores
        scores = moderation_service.get_moderation_scores(request.text)
        
        return ModerationResponse(
            scores=scores,
            requests_per_second=rps
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 