"""
app/core/config.py

This file handles application configuration using Pydantic Settings.
It validates environment variables and provides typed access to settings.

In a real production environment, these values would come from a .env file 
or environment variables injected by the orchestration platform (e.g., K8s, Docker).
"""

from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings model.
    Pydantic will automatically parse environment variables.
    """
    
    # PROJECT
    PROJECT_NAME: str = "FastAPI Production Template"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    # In production, generate a strong random key!
    # Run: openssl rand -hex 32
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" 
    ALGORITHM: str = "HS256"
    # Access token expiration time (minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # SYSTEM / INTERNAL
    # Secure API Key for Cron Jobs or Internal Microservices
    # In production, this should be secret and rotated regularly.
    API_KEY: str = "internal_secret_key_12345"
    
    # CORS
    # List of allowed origins for Cross-Origin Resource Sharing
    # In production, this should be the exact domain of your frontend
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Validates and parses the CORS origins.
        Accepts a comma-separated string or a list.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        # env_file = ".env"  # Uncomment to load from .env file

# Instantiate settings to be imported throughout the app
settings = Settings()
