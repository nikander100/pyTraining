from fastapi import APIRouter
from ..utils import work
import time

router = APIRouter()

@router.get("/slow", tags=["slow"])
async def slow():
    start = time.monotonic()
    await work.simulate()
    elapsed = time.monotonic() - start
    
    return {
        "status": "ok",
        "time_taken_seconds": elapsed
    }