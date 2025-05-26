from transformers import pipeline
from fastapi import HTTPException
from src.utils.logger import setup_app_logger
from src.moderation.models import TextRequest, ModerationResponse, HealthResponse
from src.core.tracking.request_tracker import RequestTracker
from src.config import MODEL_NAME

logger = setup_app_logger(__name__)

class ModerationService:
    def __init__(self):
        self.model = pipeline("text-classification", model=MODEL_NAME)
        self.request_tracker = RequestTracker()
        logger.info(f"Moderation model {MODEL_NAME} loaded successfully")
    
    async def moderate_text(self, request: TextRequest) -> ModerationResponse:
        """
        Moderate text content using AI model.
        
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
            result = self.model(request.text)
            scores = {item['label']: item['score'] for item in result}
            return ModerationResponse(scores=scores)
        except Exception as e:
            logger.error(f"Error in moderation: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def check_health(self) -> HealthResponse:
        """
        Check the health of the moderation service.
        
        Returns:
            HealthResponse indicating service status
        """
        try:
            if not self.model:
                raise Exception("Model not loaded")
            return HealthResponse()
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise HTTPException(status_code=503, detail="Service unhealthy") 