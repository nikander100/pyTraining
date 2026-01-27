from fastapi import FastAPI
from prometheus_client import make_asgi_app
from .routers import error, slow, health
from .middleware import logging, metrics

app = FastAPI()
app.mount("/metrics", make_asgi_app(), "Metrics App")

app.include_router(error.router)
app.include_router(slow.router)
app.include_router(health.router)

app.middleware("http")(metrics.logRequestCount)
app.middleware("http")(logging.logRequests)

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