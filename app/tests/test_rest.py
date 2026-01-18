import pytest
from httpx import AsyncClient, ASGITransport
from app.src.main import app

@pytest.mark.asyncio
async def testsSlowRoute():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/")
    
    assert resp.status_code == 200
    assert resp.json()["message"] == "Hello TomTom"


@pytest.mark.asyncio
async def testsSlowRoute():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/teapot")

    assert resp.status_code == 418
    assert resp.json()["status"] == "I'm a teapot"