"""
app/schemas/user.py

Pydantic models for User data.
We separate "Schemas" (Pydantic models) from "Database Models" (ORM models).
Since we are using an in-memory dict, these act as both validation and serialization layers.

Structure:
- UserBase: Shared properties
- UserCreate: Properties to receive on creation
- UserUpdate: Properties to receive on update
- User: Properties to return to client
"""

from typing import Optional
from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
