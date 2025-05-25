from transformers import pipeline
from src.utils.logger import setup_app_logger
from src.moderation.models import TextRequest

logger = setup_app_logger(__name__)

class ModerationService:
    def __init__(self):
        self.model = pipeline("text-classification", model="KoalaAI/Text-Moderation")
        logger.info("Moderation model loaded successfully")
    
    def get_moderation_scores(self, request: TextRequest) -> dict:
        """
        Get moderation scores for the given text.
        
        Args:
            request: TextRequest containing the text to moderate
            
        Returns:
            Dictionary of moderation scores
            
        Raises:
            Exception: If moderation fails
        """
        try:
            # Text is already validated by Pydantic
            result = self.model(request.text)
            return {item['label']: item['score'] for item in result}
        except Exception as e:
            logger.error(f"Error in moderation: {str(e)}")
            raise 