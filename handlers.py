from fastapi import HTTPException
from service import ModerationService
from tracker import RequestTracker
from logger_config import setup_logger
from models import TextRequest, ModerationResponse

logger = setup_logger(__name__)

class ModerationHandler:
    def __init__(self):
        self.moderation_service = ModerationService()
        self.request_tracker = RequestTracker()
    
    async def handle_moderation(self, request: TextRequest) -> ModerationResponse:
        # Track request
        self.request_tracker.add_request()
        
        # Log request rates with human-readable timestamps
        stats = self.request_tracker.get_formatted_stats()
        logger.info(f"Request rates - 1s: {len(stats['1s'])}, 1m: {len(stats['1m'])}, 1h: {len(stats['1h'])}")
        logger.info(f"Recent requests - 1s: {stats['1s']}")
        
        try:
            # Get moderation scores
            scores = self.moderation_service.get_moderation_scores(request.text)
            return ModerationResponse(scores=scores)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e)) 