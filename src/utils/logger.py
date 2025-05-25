import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Set up and configure a logger with rotation.
    
    Args:
        name: The name of the logger (typically __name__ from the calling module)
        
    Returns:
        A configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # Configure logging with rotation
    log_handler = RotatingFileHandler(
        'logs/app.log',           # Log file path
        maxBytes=1024*1024,       # 1MB per file
        backupCount=5,            # Keep 5 backup files
        encoding='utf-8'
    )
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    
    return logger 