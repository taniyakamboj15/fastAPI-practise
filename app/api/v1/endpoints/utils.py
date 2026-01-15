"""
app/api/v1/endpoints/utils.py

Internal Utility Endpoints.
These are protected by API Key, not User Token.
Used for cron jobs, health checks, or internal maintenance.
"""

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
    """
    Internal health check or maintenance trigger.
    Only accessible with X-API-Key header.
    """
    return {"status": "ok", "maintenance_mode": False}

@router.post("/test-email")
def test_email_send(
    email_to: EmailStr,
    api_key: str = Depends(deps.get_api_key)
) -> Any:
    """
    Test email sending functionality (Mock).
    """
    return {"msg": f"Test email sent to {email_to}"}
