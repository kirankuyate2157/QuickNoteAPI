from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        method = request.method
        path = request.url.path
        status_code = response.status_code

        print(f"[LOG] {method} {path} → {status_code} ({process_time:.2f}ms)")

        return response