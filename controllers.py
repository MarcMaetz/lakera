from fastapi import APIRouter
from models import TextRequest, ModerationResponse
from handlers import ModerationHandler

router = APIRouter()
moderation_handler = ModerationHandler()

@router.post("/moderate", response_model=ModerationResponse)
async def moderate_text(request: TextRequest):
    return await moderation_handler.handle_moderation(request) 