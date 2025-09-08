import os
from urllib.parse import urlparse

def get_railway_database_url():
    """Get database URL for Railway deployment"""
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Railway provides DATABASE_URL in format: postgresql://user:pass@host:port/db
        return database_url
    else:
        # Fallback to SQLite for local development
        return "sqlite:///./seleciona_ai.db"

def get_railway_settings():
    """Get settings optimized for Railway"""
    return {
        "database_url": get_railway_database_url(),
        "host": "0.0.0.0",
        "port": int(os.getenv("PORT", "8000")),
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "secret_key": os.getenv("SECRET_KEY", "change-this-in-production"),
        "algorithm": "HS256",
        "access_token_expire_minutes": 30
    } 