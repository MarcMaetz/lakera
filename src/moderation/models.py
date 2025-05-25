from pydantic import BaseModel, Field, validator
from typing import Dict

class TextRequest(BaseModel):
    """Request model for text moderation"""
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Text to be moderated",
        example="This is a sample text to moderate"
    )

    @validator('text')
    def normalize_text(cls, v: str) -> str:
        """Normalize text by removing excessive whitespace"""
        return " ".join(v.split())

class ModerationResponse(BaseModel):
    """Response model containing moderation scores"""
    scores: Dict[str, float] = Field(
        ...,
        description="Dictionary of moderation category scores",
        example={
            "toxic": 0.1,
            "hate": 0.05,
            "harassment": 0.02
        }
    )

    @validator('scores')
    def validate_scores(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Validate that all scores are between 0 and 1"""
        for category, score in v.items():
            if not 0 <= score <= 1:
                raise ValueError(f"Score for {category} must be between 0 and 1")
        return v 