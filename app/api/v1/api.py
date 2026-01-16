"""
app/api/v1/api.py

This file aggregates all router endpoints into a single core router.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, items, utils, demo_db, demo_tasks

api_router = APIRouter()

# Include sub-routers.
# tags=["some_tag"] helps group generic endpoints in Swagger UI.
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(demo_db.router, prefix="/demo", tags=["demo-db"])
api_router.include_router(demo_tasks.router, prefix="/demo-tasks", tags=["demo-tasks"])
