from fastapi import HTTPException
from src.utils.logger import setup_app_logger
from src.moderation.models import TextRequest, ModerationResponse, HealthResponse
from src.moderation.service import ModerationService
from src.core.tracking.request_tracker import RequestTracker

logger = setup_app_logger(__name__)

class ModerationHandler:
    def __init__(self):
        self.service = ModerationService()
        self.request_tracker = RequestTracker()
    
    async def handle_moderation(self, request: TextRequest) -> ModerationResponse:
        """
        Handle text moderation request.
        
        Args:
            request: TextRequest containing the text to moderate
            
        Returns:
            ModerationResponse containing the moderation scores
            
        Raises:
            HTTPException: If moderation fails
        """
        try:
            # Track request
            self.request_tracker.add_request()
            
            # Process moderation
            scores = self.service.get_moderation_scores(request)
            return ModerationResponse(scores=scores)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def check_health(self) -> HealthResponse:
        """
        Check the health of the moderation service.
        
        Returns:
            HealthResponse indicating service status
        """
        try:
            # Basic health check - verify model is loaded
            if not self.service.model:
                raise Exception("Model not loaded")
            return HealthResponse()
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise HTTPException(status_code=503, detail="Service unhealthy") 