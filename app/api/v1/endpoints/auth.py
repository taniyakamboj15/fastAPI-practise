
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response

from app.core import security
from app.core.config import settings
from app.api import deps
from app.schemas import user as user_schema
from app.db.session import SessionLocal
from sqlmodel import Session, select
from app.models.user import User

router = APIRouter()

@router.post("/login/access-token")
def login_access_token(
    response: Response,
    user_in: user_schema.UserLogin,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Login endpoint that sets an HttpOnly cookie with the JWT.
    Accepts JSON body: { "email": "...", "password": "..." }
    """
    
    # Authenticate User
    statement = select(User).where(User.email == user_in.email)
    user = db.exec(statement).first()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not security.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    # Set HttpOnly Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
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
