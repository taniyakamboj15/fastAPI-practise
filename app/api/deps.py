"""
app/api/deps.py

This module contains FastAPI dependencies.
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from pydantic import ValidationError

from app.core.config import settings
from app.core import security
from app.schemas import user as user_schema
from app.schemas import token as token_schema
from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    Dependency to get the database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_token_from_cookie(request: Request) -> str:
    """
    Extracts the token from the HttpOnly cookie.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return token

from sqlmodel import Session, select
from app.models.user import User

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_token_from_cookie)
) -> user_schema.User:
    """
    Dependency to get the current authenticated user from the JWT token in Cookie.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = token_schema.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = None
    if token_data.sub:
        if token_data.sub.isdigit():
             user = db.get(User, int(token_data.sub))
        
        if not user:
             # Fallback to lookup by email if sub wasn't an ID or ID lookup failed
             # (Assuming sub could be email in some legacy system, though typically it's ID)
             # In our code, we use email as username usually, but sub is usually ID. 
             # Let's support email lookup for robustness if ID fails or isn't digit.
             statement = select(User).where(User.email == token_data.sub)
             results = db.exec(statement)
             user = results.first()
        
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user # User model is compatible with User schema

def get_current_active_user(
    current_user: user_schema.User = Depends(get_current_user),
) -> user_schema.User:
    """
    Verifies that the current user is active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: user_schema.User = Depends(get_current_active_user),
) -> user_schema.User:
    """
    Verifies that the current user is a superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

# API Key Security Scheme
from fastapi.security import APIKeyHeader
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(
    api_key_header: str = Depends(api_key_header),
) -> str:
    """
    Validates the API Key from the 'X-API-Key' header.
    Used for machine-to-machine communication (Cron jobs, Internal Microservices).
    """
    if api_key_header == settings.API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )
