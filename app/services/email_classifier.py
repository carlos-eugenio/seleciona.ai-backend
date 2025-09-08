import os
from typing import Tuple
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from app.config import settings
from app.utils.preprocessing import email_preprocessor
from app.utils.portuguese_config import (
    PRODUCTIVE_RESPONSES, 
    UNPRODUCTIVE_RESPONSES,
    PORTUGUESE_MODEL_CONFIG
)

class EmailClassifier:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.classifier = None
        self.use_ml_model = settings.use_ml_model
        if self.use_ml_model:
            self._load_model()
    
    def _load_model(self):
        """Load the pre-trained model for email classification"""
        try:
            # Use Portuguese model configuration
            model_name = PORTUGUESE_MODEL_CONFIG["primary_model"]
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name, 
                num_labels=2
            )
            
            # Create a pipeline for text classification
            self.classifier = pipeline(
                "text-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            print(f"Error loading Portuguese model: {e}")
            try:
                # Fallback to multilingual model
                model_name = PORTUGUESE_MODEL_CONFIG["fallback_model"]
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    model_name, 
                    num_labels=2
                )
                
                self.classifier = pipeline(
                    "text-classification",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device=0 if torch.cuda.is_available() else -1
                )
            except Exception as e2:
                print(f"Error loading multilingual model: {e2}")
                # Fallback to rule-based classification
                self.classifier = None
    
    def toggle_ml_model(self, enable: bool):
        """Toggle between ML model and rule-based classification"""
        self.use_ml_model = enable
        if enable and not self.classifier:
            self._load_model()
        elif not enable:
            # Optionally unload model to free memory
            self.classifier = None
            self.model = None
            self.tokenizer = None
    
    def classify_email(self, subject: str, message: str) -> Tuple[str, str]:
        """
        Classify email as productive or unproductive
        Returns: (classification, response)
        """
        # Preprocess the text (always active for analysis)
        processed_text = email_preprocessor.extract_features(subject, message)
        
        if not processed_text.strip():
            return "UNPRODUCTIVE", "Este email parece estar vazio ou não contém conteúdo significativo."
        
        # Choose classification method based on toggle
        if self.use_ml_model and self.classifier:
            try:
                result = self.classifier(processed_text)
                confidence = result[0]['score']
                label = result[0]['label']
                
                # Convert model output to our classification
                confidence_threshold = PORTUGUESE_MODEL_CONFIG["confidence_threshold"]
                if label == 'LABEL_1' or confidence > confidence_threshold:
                    classification = "PRODUCTIVE"
                    response = self._generate_productive_response(subject, message)
                else:
                    classification = "UNPRODUCTIVE"
                    response = self._generate_unproductive_response(subject, message)
                    
            except Exception as e:
                print(f"ML classification failed: {e}")
                # Fallback to rule-based
                classification, response = self._rule_based_classification(subject, message)
        else:
            # Use rule-based classification
            classification, response = self._rule_based_classification(subject, message)
        
        return classification, response
    
    def _rule_based_classification(self, subject: str, message: str) -> Tuple[str, str]:
        """Rule-based classification using keyword matching"""
        combined_text = f"{subject} {message}".lower()
        
        # Check for productive indicators
        if email_preprocessor.is_productive_keywords(combined_text):
            return "PRODUCTIVE", self._generate_productive_response(subject, message)
        
        # Check for unproductive indicators
        if email_preprocessor.is_unproductive_keywords(combined_text):
            return "UNPRODUCTIVE", self._generate_unproductive_response(subject, message)
        
        # Default to productive if unclear
        return "PRODUCTIVE", self._generate_productive_response(subject, message)
    
    def _generate_productive_response(self, subject: str, message: str) -> str:
        """Generate response for productive emails"""
        # Simple response selection based on subject length
        response_index = len(subject) % len(PRODUCTIVE_RESPONSES)
        return PRODUCTIVE_RESPONSES[response_index].format(subject=subject)
    
    def _generate_unproductive_response(self, subject: str, message: str) -> str:
        """Generate response for unproductive emails"""
        # Simple response selection based on subject length
        response_index = len(subject) % len(UNPRODUCTIVE_RESPONSES)
        return UNPRODUCTIVE_RESPONSES[response_index]

# Global instance
email_classifier = EmailClassifier()
