import logging, pytest
from httpx import AsyncClient, ASGITransport
from app.src.main import app

@pytest.mark.asyncio
async def testLoggingMiddlewareFields(caplog, monkeypatch):
    monkeypatch.setattr("app.src.logging_conf.logger.propagate", True)
    caplog.set_level(logging.INFO, logger="app")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/")

    assert resp.status_code == 200
    records = [r for r in caplog.records if r.name == "app"]
    assert records, "no logs from app logger"
    rec = records[-1]
    assert rec.endpoint == "/"
    assert rec.status_code == 200
    assert rec.latency is not None
    assert rec.error_message is None
    assert hasattr(rec, "client_ip")
    assert hasattr(rec, "user_agent")