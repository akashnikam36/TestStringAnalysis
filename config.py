from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):    
    # Maximum allowed input size in characters (10,000 characters ~= 2000 words)
    MAX_INPUT_SIZE: int = 10000
    
    # API Configuration
    API_TITLE: str = "String Analysis API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "A production-grade API for analyzing text strings"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    # CORS Configuration (configure properly for production)
    CORS_ORIGINS: list = ["*"]
