from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./seleciona_ai.db"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File uploads
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = [".txt", ".pdf"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Railway environment variables
if os.getenv("DATABASE_URL"):
    # Railway provides DATABASE_URL in format: postgresql://user:pass@host:port/db
    Settings.database_url = os.getenv("DATABASE_URL")

if os.getenv("PORT"):
    Settings.port = int(os.getenv("PORT"))

if os.getenv("SECRET_KEY"):
    Settings.secret_key = os.getenv("SECRET_KEY")

settings = Settings()
