"""
TutorAgent MVP Configuration Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Optional
import os
import json
from pathlib import Path


class Settings(BaseSettings):
    """Application settings configuration."""
    
    # Application Settings
    APP_NAME: str = "TutorAgent"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://tutor_user:tutor_password@localhost:5432/tutor_agent_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "tutor_agent_db"
    DB_USER: str = "tutor_user"
    DB_PASSWORD: str = "tutor_password"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # LLM API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # File Storage Configuration
    UPLOAD_DIR: str = "./data/uploads"
    PROCESSED_DIR: str = "./data/processed"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "png", "jpg", "jpeg"]
    
    # OCR Configuration
    OCR_ENGINE: str = "paddleocr"  # paddleocr or tesseract
    OCR_LANGUAGE: str = "en"
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    
    # Session Configuration
    SESSION_TIMEOUT: int = 3600  # 1 hour
    MAX_QUESTIONS_PER_SESSION: int = 20
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "./logs/tutor_agent.log"
    
    # Frontend Configuration
    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Security Settings - can be overridden by environment variable
    ALLOW_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://tutor-agent-nsw-git-main-voturi-gmailcoms-projects.vercel.app",
        "https://tutor-agent-nsw.vercel.app"
    ]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    ALLOW_HEADERS: List[str] = ["*"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Monitoring and Analytics
    SENTRY_DSN: Optional[str] = None
    ANALYTICS_ENABLED: bool = True
    
    # Development Settings
    RELOAD: bool = True
    WORKERS: int = 1
    
    model_config = SettingsConfigDict(
        env_file=[".env", "../.env"],  # Look for .env in current dir and parent dir
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Ensure directories exist
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"
    
    @field_validator('ALLOW_ORIGINS', mode='before')
    @classmethod
    def parse_allow_origins(cls, v):
        """Parse ALLOW_ORIGINS from environment variable (JSON string or list)."""
        if isinstance(v, str):
            try:
                # Try to parse as JSON
                return json.loads(v)
            except json.JSONDecodeError:
                # If not JSON, split by comma
                return [origin.strip() for origin in v.split(',')]
        return v


# Create global settings instance
settings = Settings()
