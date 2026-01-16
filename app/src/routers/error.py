from fastapi import APIRouter

router = APIRouter()

@router.get("/error", status_code=500, tags=["Error"])
async def error():
    return {
        "status": "500"
    }