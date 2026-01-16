import pytest
from httpx import AsyncClient, ASGITransport
from app.src.main import app

async def _fake_sim():
    return None

@pytest.mark.asyncio
async def test_slow_route(monkeypatch):
    monkeypatch.setattr("app.src.utils.work.simulate", _fake_sim)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/slow")
        
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert isinstance(data["time_taken_seconds"], float)
    assert data["time_taken_seconds"] >= 0.0
