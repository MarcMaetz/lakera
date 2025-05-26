from fastapi import APIRouter
from src.moderation.models import TextRequest, ModerationResponse, HealthResponse
from src.moderation.service import ModerationService

class ModerationController:
    def __init__(self):
        self.service = ModerationService()
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.get("/health", response_model=HealthResponse)
        async def health_check():
            return await self.service.check_health()

        @self.router.post("/moderate", response_model=ModerationResponse)
        async def moderate_text(request: TextRequest):
            return await self.service.moderate_text(request)

# Create router instance
moderation_controller = ModerationController()
router = moderation_controller.router 