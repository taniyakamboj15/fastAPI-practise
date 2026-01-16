from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
   
    # PROJECT
    PROJECT_NAME: str = "FastAPI Production Template"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" 
    ALGORITHM: str = "HS256"
    # Access token expiration time (minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # SYSTEM / INTERNAL
    API_KEY: str = "internal_secret_key_12345"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # DATABASE
    # PostgreSQL Connection String
    # Format: postgresql://user:password@postgresserver/db
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:@localhost:5432/my_db"

    # CELERY / REDIS
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
       
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
