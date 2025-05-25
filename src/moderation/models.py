from pydantic import BaseModel
from typing import Dict

class TextRequest(BaseModel):
    """Request model for text moderation"""
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "This is a sample text to moderate"
            }
        }

class ModerationResponse(BaseModel):
    """Response model containing moderation scores"""
    scores: Dict[str, float]

    class Config:
        schema_extra = {
            "example": {
                "scores": {
                    "toxic": 0.1,
                    "hate": 0.05,
                    "harassment": 0.02
                }
            }
        } 