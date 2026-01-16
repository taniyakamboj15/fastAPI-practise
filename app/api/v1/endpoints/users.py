
from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from app.api import deps
from app.core import security
from app.schemas import user as user_schema
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[user_schema.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: user_schema.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    Only superusers can see all users.
    """
    statement = select(User).offset(skip).limit(limit)
    users = db.exec(statement).all()
    return users

@router.post("/", response_model=user_schema.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schema.UserCreate,
) -> Any:
   
    statement = select(User).where(User.email == user_in.email)
    user_exists = db.exec(statement).first()
    
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    hashed_password = security.get_password_hash(user_in.password)
    
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        is_active=True,
        is_superuser=False
    )
    

    count_statement = select(User)
    first_user = db.exec(count_statement).first()
    if not first_user:
        db_user.is_superuser = True

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating user."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get("/me", response_model=user_schema.User)
def read_user_me(
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:

    return current_user

@router.put("/me", response_model=user_schema.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schema.UserUpdate,
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:
   
    db_user = db.get(User, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_in.dict(exclude_unset=True)
    if "password" in user_data and user_data["password"]:
        hashed_password = security.get_password_hash(user_data["password"])
        del user_data["password"]
        db_user.hashed_password = hashed_password
        
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
