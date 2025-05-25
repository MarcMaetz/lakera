from transformers import pipeline
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ModerationService:
    def __init__(self):
        self.model = pipeline("text-classification", model="KoalaAI/Text-Moderation")
        logger.info("Moderation model loaded successfully")
    
    def get_moderation_scores(self, text: str) -> dict:
        """
        Get moderation scores for the given text.
        
        Args:
            text: The text to moderate
            
        Returns:
            Dictionary of moderation scores
        """
        try:
            result = self.model(text)
            return {item['label']: item['score'] for item in result}
        except Exception as e:
            logger.error(f"Error in moderation: {str(e)}")
            raise 