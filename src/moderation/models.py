from pydantic import BaseModel
from typing import Dict

class TextRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    scores: Dict[str, float] 