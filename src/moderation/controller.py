from fastapi import APIRouter
from src.moderation.models import TextRequest, ModerationResponse
from src.moderation.api import ModerationAPI

class ModerationController:
    def __init__(self):
        self.api = ModerationAPI()
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.post("/moderate", response_model=ModerationResponse)
        async def moderate_text(request: TextRequest):
            return await self.api.handle_moderation(request)

# Create router instance
moderation_controller = ModerationController()
router = moderation_controller.router 