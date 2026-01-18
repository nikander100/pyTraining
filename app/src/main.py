from fastapi import FastAPI, Request, HTTPException, Response
from .routers import error, slow, health
from .logging_conf import logger
import time, uuid, json

app = FastAPI()
app.include_router(error.router)
app.include_router(slow.router)
app.include_router(health.router)

@app.middleware("http")
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

        if status_code >= 400:
            try:
                body = getattr(response, "body", b"")
                if isinstance(body, (bytes, bytearray)):
                    parsed = json.loads(body.decode() or "{}")
                    error_message = parsed.get("detail")
            except Exception:
                error_message = None

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

@app.get("/")
async def root():
    return {
        "message": "Hello TomTom"
    }

@app.get("/teapot", status_code=418)
async def teapot():
    return {
        "status": "I'm a teapot"
    }