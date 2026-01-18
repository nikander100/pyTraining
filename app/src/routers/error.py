from fastapi import APIRouter

router = APIRouter()

@router.get("/error", status_code=500, tags=["error"])
async def error():
    return {
        "status": "error"
    }