
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
   
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_token_from_cookie(request: Request) -> str:
   
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

             statement = select(User).where(User.email == token_data.sub)
             results = db.exec(statement)
             user = results.first()
        
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user 

def get_current_active_user(
    current_user: user_schema.User = Depends(get_current_user),
) -> user_schema.User:
  
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: user_schema.User = Depends(get_current_active_user),
) -> user_schema.User:
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

from fastapi.security import APIKeyHeader
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(
    api_key_header: str = Depends(api_key_header),
) -> str:
   
    if api_key_header == settings.API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )
