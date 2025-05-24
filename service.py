from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict

class ModerationService:
    def __init__(self):
        # Load model and tokenizer
        self.model_name = "KoalaAI/Text-Moderation"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=False)  # Disable fast tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
        # Get label names from model config
        self.labels = self.model.config.id2label
        
    def get_moderation_scores(self, text: str) -> Dict[str, float]:
        # Tokenize input
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.sigmoid(outputs.logits).squeeze().numpy()
        
        # Convert scores to dictionary with label names
        result = {
            self.labels[i]: float(score)
            for i, score in enumerate(scores)
        }
        
        return result 