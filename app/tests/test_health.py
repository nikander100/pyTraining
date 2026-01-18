import pytest
from httpx import AsyncClient, ASGITransport
from app.src.main import app

@pytest.mark.asyncio
async def testHealthRouteHealthy(monkeypatch):
    monkeypatch.setattr("app.src.routers.health.random.random", lambda: 1)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/health")

    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

@pytest.mark.asyncio
async def testHealthRouteUnhealthy(monkeypatch):
    monkeypatch.setattr("app.src.routers.health.random.random", lambda: 0)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/health")

    assert resp.status_code == 500
    assert resp.json()["detail"] == "unhealty"
