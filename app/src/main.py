from fastapi import FastAPI
from .routers import error, slow, health

app = FastAPI()
app.include_router(error.router)
app.include_router(slow.router)
app.include_router(health.router)

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