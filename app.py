from fastapi import FastAPI, HTTPException
import uvicorn
from service import ModerationService
from tracker import RequestTracker
from logger_config import setup_logger
from models import TextRequest, ModerationResponse

# Set up logger
logger = setup_logger(__name__)

app = FastAPI(title="Content Moderation API")
moderation_service = ModerationService()
request_tracker = RequestTracker()

@app.post("/moderate", response_model=ModerationResponse)
async def moderate_text(request: TextRequest):
    # Track request
    request_tracker.add_request()
    
    # Log request rates with human-readable timestamps
    stats = request_tracker.get_formatted_stats()
    logger.info(f"Request rates - 1s: {len(stats['1s'])}, 1m: {len(stats['1m'])}, 1h: {len(stats['1h'])}")
    logger.info(f"Recent requests - 1s: {stats['1s']}")
    
    try:
        # Get moderation scores
        scores = moderation_service.get_moderation_scores(request.text)
        
        return ModerationResponse(scores=scores)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 