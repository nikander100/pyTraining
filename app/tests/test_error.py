import pytest
from httpx import AsyncClient, ASGITransport
from app.src.main import app

@pytest.mark.asyncio
async def testsSlowRoute():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/error")

    assert resp.status_code == 500
    assert resp.json()["status"] == "error"
