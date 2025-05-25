from fastapi import APIRouter, HTTPException
from src.core.tracking.request_tracker import RequestTracker
from src.utils.logger import setup_app_logger
from src.moderation.models import TextRequest, ModerationResponse
from src.moderation.service import ModerationService

logger = setup_app_logger(__name__)

class ModerationAPI:
    def __init__(self):
        self.moderation_service = ModerationService()
        self.request_tracker = RequestTracker()
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.post("/moderate", response_model=ModerationResponse)
        async def moderate_text(request: TextRequest):
            # Track request
            self.request_tracker.add_request()
            
            try:
                # Get moderation scores
                scores = self.moderation_service.get_moderation_scores(request.text)
                return ModerationResponse(scores=scores)
            except Exception as e:
                logger.error(f"Error processing request: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

# Create router instance
moderation_api = ModerationAPI()
router = moderation_api.router 