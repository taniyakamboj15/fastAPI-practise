
from typing import Any
from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api import deps
from app.core.config import settings
from app.schemas import user as user_schema

router = APIRouter()

@router.get("/health-check")
def health_check(
    api_key: str = Depends(deps.get_api_key)
) -> Any:
   
    return {"status": "ok", "maintenance_mode": False}

@router.post("/test-email")
def test_email_send(
    email_to: EmailStr,
    api_key: str = Depends(deps.get_api_key)
) -> Any:
   
    return {"msg": f"Test email sent to {email_to}"}
