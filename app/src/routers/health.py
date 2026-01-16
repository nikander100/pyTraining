from fastapi import APIRouter, HTTPException
import random

router = APIRouter()

@router.get("/health", tags=["health"])
async def health():
    if random.random() < 0.05:
        raise HTTPException(status_code=500, detail="unhealty")
    return {
        "status": "ok"
    }