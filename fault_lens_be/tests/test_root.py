import pytest


@pytest.mark.asyncio
async def test_root_returns_application_status(client):
    response = await client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["application"] == "FaultLens API"