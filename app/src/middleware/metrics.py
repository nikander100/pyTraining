from fastapi import Request, HTTPException, Response
import time
from ..metrics_conf import REQUEST_COUNT, REQUEST_TIME

async def logRequestCount(request: Request, call_next):
    if request.url.path.startswith("/metrics"):
        return await call_next(request)
    start = time.monotonic()
    
    method = request.method
    status_code = 500
    try:
        response: Response = await call_next(request)
        status_code = response.status_code
        return response

    except HTTPException as excp:
        status_code = excp.status_code
        raise
    except Exception:
        status_code = 500
        raise
    finally:
        route = request.scope.get("route")
        endpoint = route.path if route else "not_found"
        endpoint_error = "true" if status_code >= 400 else "false"
        latency = time.monotonic() - start
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, endpoint_error=endpoint_error).inc()
        REQUEST_TIME.labels(method=method, endpoint=endpoint).observe(latency)