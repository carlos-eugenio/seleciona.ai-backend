import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string
from typing import List, Tuple
from .portuguese_config import (
    PRODUCTIVE_KEYWORDS, 
    UNPRODUCTIVE_KEYWORDS,
    PORTUGUESE_PREPROCESSING_CONFIG
)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Download Portuguese data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/floresta')
except LookupError:
    nltk.download('floresta')

class EmailPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        # Use Portuguese stopwords
        try:
            self.stop_words = set(stopwords.words('portuguese'))
        except LookupError:
            # Fallback to English if Portuguese not available
            self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_and_stem(self, text: str) -> List[str]:
        """Tokenize text and apply stemming"""
        if not text:
            return []
            
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stop words and apply stemming
        processed_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                stemmed = self.stemmer.stem(token)
                processed_tokens.append(stemmed)
        
        return processed_tokens
    
    def extract_features(self, subject: str, message: str) -> str:
        """Extract and combine features from subject and message"""
        # Clean both subject and message
        clean_subject = self.clean_text(subject)
        clean_message = self.clean_text(message)
        
        # Combine subject and message
        combined_text = f"{clean_subject} {clean_message}"
        
        # Tokenize and stem
        features = self.tokenize_and_stem(combined_text)
        
        return " ".join(features)
    
    def is_productive_keywords(self, text: str) -> bool:
        """Check for keywords that indicate productive emails"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in PRODUCTIVE_KEYWORDS)
    
    def is_unproductive_keywords(self, text: str) -> bool:
        """Check for keywords that indicate unproductive emails"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in UNPRODUCTIVE_KEYWORDS)

# Global instance
email_preprocessor = EmailPreprocessor()
