from fastapi import FastAPI
from .routers import error, slow, health
from .middleware.logging import logRequests

app = FastAPI()
app.include_router(error.router)
app.include_router(slow.router)
app.include_router(health.router)

app.middleware("http")(logRequests)

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