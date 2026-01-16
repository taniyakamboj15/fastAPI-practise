
import time
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestIDMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

class LogRequestMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        
        
        request_id = getattr(request.state, "request_id", "limitless")

        logger.info(
            f"id={request_id} "
            f"method={request.method} "
            f"path={request.url.path} "
            f"status={response.status_code} "
            f"duration={formatted_process_time}ms"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
