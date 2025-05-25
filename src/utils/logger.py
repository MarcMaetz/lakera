import logging
from logging.handlers import RotatingFileHandler
import os

def _setup_log_handler(log_file: str, formatter: logging.Formatter) -> RotatingFileHandler:
    """Helper function to create a rotating file handler with common settings"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    handler = RotatingFileHandler(
        f'logs/{log_file}',
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    handler.setFormatter(formatter)
    return handler

def setup_rps_logger() -> logging.Logger:
    """Set up a logger specifically for RPS tracking"""
    logger = logging.getLogger('rps')
    logger.setLevel(logging.INFO)

    # Only add handler if it hasn't been added yet
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler = _setup_log_handler('rps.log', formatter)
        logger.addHandler(handler)
    
    return logger

def setup_app_logger(name: str) -> logging.Logger:
    """Set up a logger for general application logging"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Only add handler if it hasn't been added yet
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = _setup_log_handler('app.log', formatter)
        logger.addHandler(handler)
    
    return logger 