import pytest


@pytest.mark.asyncio
async def test_database_health(client):
    response = await client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {
        "status":"ok",
        "database": "connected"
    }