"""
app/api/v1/endpoints/users.py

User CRUD operations.
"""

from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from app.api import deps
from app.core import security
from app.schemas import user as user_schema
from app.db.session import db

router = APIRouter()

@router.get("/", response_model=List[user_schema.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: user_schema.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    Only superusers can see all users.
    """
    users = db.get_users()
    return users[skip : skip + limit]

@router.post("/", response_model=user_schema.User)
def create_user_open(
    *,
    user_in: user_schema.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in (Registration).
    """
    user_exists = db.get_user_by_email(user_in.email)
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # Create new user
    user_data = jsonable_encoder(user_in)
    del user_data["password"] # don't store plain password
    user_data["hashed_password"] = security.get_password_hash(user_in.password)
    user_data["is_active"] = True
    user_data["is_superuser"] = False # Default to normal user
    
    # If this is the FIRST user, allow them to be superuser for demo purposes
    if not db.users:
        user_data["is_superuser"] = True

    new_user = db.create_user(user_data)
    return new_user

@router.get("/me", response_model=user_schema.User)
def read_user_me(
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=user_schema.User)
def update_user_me(
    *,
    user_in: user_schema.UserUpdate,
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user_data = db.users[current_user.id] # retrieve raw dict
    
    # Update fields
    if user_in.password:
        user_data["hashed_password"] = security.get_password_hash(user_in.password)
    if user_in.full_name:
        user_data["full_name"] = user_in.full_name
    if user_in.email:
        user_data["email"] = user_in.email
        
    db.users[current_user.id] = user_data
    return user_data
