"""
app/main.py

Main application entry point.
Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

# Initialize FastAPI application
# title: Title in Swagger UI
# openapi_url: URL for OpenAPI schema (json)
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include the main API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    """
    Example of setting a CUSTOM HEADER.
    This middleware calculates the time taken to process the request
    and adds it as a header 'X-Process-Time' to the response.
    
    Why used?
    - Debugging latency issues.
    - Monitoring performance.
    """
    import time
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate duration
    process_time = time.time() - start_time
    
    # SET CUSTOM HEADER HERE
    # This header will be visible in the Network tab of the browser
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.get("/")
def root():
    """
    Simples route to verify the app is running.
    """
    return {"message": "Welcome to the FastAPI Production Template"}
