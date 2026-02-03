"""Application configuration and settings."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_KEY: str = "your-secret-api-key-change-in-production"
    API_TITLE: str = "AI Voice Detection API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Production-grade API for AI-generated voice detection"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Audio Processing Configuration
    AUDIO_DOWNLOAD_TIMEOUT: int = 30
    MAX_AUDIO_DURATION_SECONDS: int = 60
    SUPPORTED_AUDIO_FORMATS: list[str] = [".mp3", ".wav", ".m4a", ".flac"]
    SAMPLE_RATE: int = 16000
    
    # Model Configuration
    MODEL_VERSION: str = "1.0.0"
    MODEL_PATH: Optional[str] = None
    
    # Temporary file storage
    TEMP_DIR: str = "/tmp/audio_processing"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

