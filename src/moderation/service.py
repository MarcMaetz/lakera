from transformers import pipeline
from src.utils.logger import setup_app_logger
from src.moderation.models import TextRequest
from src.config import MODEL_NAME

logger = setup_app_logger(__name__)

class ModerationService:
    def __init__(self):
        self.model = pipeline("text-classification", model=MODEL_NAME)
        logger.info(f"Moderation model {MODEL_NAME} loaded successfully")
    
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
            # Get raw model output
            result = self.model(request.text)
            print(f"Result type: {type(result)}")
            print(f"Result: {result}")
            
            # Transform to dictionary
            scores = {item['label']: item['score'] for item in result}
            logger.info(f"Transformed scores: {scores}")
            
            return scores
        except Exception as e:
            logger.error(f"Error in moderation: {str(e)}")
            raise 