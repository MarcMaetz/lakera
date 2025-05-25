import logging
from logging.handlers import RotatingFileHandler
import os

def setup_rps_logger() -> logging.Logger:
    """Set up a logger specifically for RPS tracking"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    logger = logging.getLogger('rps')
    logger.setLevel(logging.INFO)

    # Only add handler if it hasn't been added yet
    if not logger.handlers:
        handler = RotatingFileHandler(
            'logs/rps.log',
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.addHandler(handler)
    
    return logger

def setup_app_logger(name: str) -> logging.Logger:
    """Set up a logger for general application logging"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Only add handler if it hasn't been added yet
    if not logger.handlers:
        handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
    
    return logger 