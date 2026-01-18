from fastapi import Request, HTTPException, Response
from ..logging_conf import logger
import time, uuid, json

async def logRequests(request: Request, call_next):
    req_id = str(uuid.uuid4())
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    start = time.monotonic()
    status_code = None
    error_message = None
    try:
        response: Response = await call_next(request)
        status_code = response.status_code
        return response

    except Exception as excp:
        if isinstance(excp, HTTPException):
            status_code = excp.status_code
            error_message = str(excp)
        else:
            status_code = 500
            error_message = str(excp)
        raise
    finally:
        latency = time.monotonic() - start
        logger.info("request completed", 
            extra={
                "request_id": req_id,
                "endpoint": request.url.path,
                "status_code": status_code,
                "latency": latency,
                "error_message": error_message,
                "client_ip": client_ip,
                "user_agent": user_agent,
        })