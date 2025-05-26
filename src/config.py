"""Configuration settings for the text moderation service"""

# Text validation settings
TEXT_MIN_LENGTH = 1
TEXT_MAX_LENGTH = 1000

# Model settings
MODEL_NAME = "KoalaAI/Text-Moderation"

# API settings
API_PREFIX = "/api/v1"
API_TITLE = "Text Moderation API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API for text moderation using AI models"

# RPS tracking settings
RPS_WINDOW_SIZE = 60  # Size of the sliding window in seconds 