"""
app/api/v1/endpoints/auth.py

Handling authentication endpoints.
Refactored to use HttpOnly Cookies for security.
"""

from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response

from app.core import security
from app.core.config import settings
from app.api import deps
from app.schemas import user as user_schema
from app.db.session import db

router = APIRouter()

@router.post("/login/access-token")
def login_access_token(
    response: Response,
    user_in: user_schema.UserLogin,
    db: Any = Depends(deps.get_db)
) -> Any:
    """
    Login endpoint that sets an HttpOnly cookie with the JWT.
    Accepts JSON body: { "email": "...", "password": "..." }
    """
    
    # We authenticate the user against our fake DB
    user_dict = db.get_user_by_email(user_in.email)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not security.verify_password(user_in.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Check if user is active
    if not user_dict.get("is_active"):
        raise HTTPException(status_code=400, detail="Inactive user")

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user_dict["id"], expires_delta=access_token_expires
    )
    
    # Set HttpOnly Cookie
    # secure=True should be used in production (HTTPS)
    # httponly=True prevents JS access (XSS protection)
    # samesite="lax" for CSRF protection
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        # secure=True, # Allow False for local dev (http)
        samesite="lax"
    )
    
    return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response) -> Any:
    """
    Logout by deleting the cookie.
    """
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}
