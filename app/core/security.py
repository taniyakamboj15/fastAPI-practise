"""
app/core/security.py

This module handles cryptographic operations:
1. Password hashing/verification using bcrypt.
2. JWT (JSON Web Token) creation for authentication.

Security best practices:
- Never store plain text passwords.
- Use strong algorithms (bcrypt) which are slow by design to resist brute-force.
- JWTs should have an expiration time to limit the window of opportunity for stolen tokens.
"""

from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Setup password hashing context
# 'bcrypt' is the hashing algorithm.
# 'deprecated="auto"' allows verifying older hashes if we migrate algorithms later.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.
    
    Args:
        subject: The subject of the token (typically user ID or username).
        expires_delta: Optional custom expiration time.
    
    Returns:
        Encoded JWT string.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Payload claims:
    # 'sub' (Subject): Who this token refers to.
    # 'exp' (Expiration Time): Handling session expiry.
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Encode with SECRET_KEY and ALGORITHM
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    Use this during login.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a password for storage.
    Use this when registering a new user.
    """
    return pwd_context.hash(password)
