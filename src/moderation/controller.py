from fastapi import APIRouter
from src.moderation.models import TextRequest, ModerationResponse, HealthResponse
from src.moderation.api import ModerationHandler

class ModerationController:
    def __init__(self):
        self.handler = ModerationHandler()
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.get("/health", response_model=HealthResponse)
        async def health_check():
            return await self.handler.check_health()

        @self.router.post("/moderate", response_model=ModerationResponse)
        async def moderate_text(request: TextRequest):
            return await self.handler.handle_moderation(request)

# Create router instance
moderation_controller = ModerationController()
router = moderation_controller.router 