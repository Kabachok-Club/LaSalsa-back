import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_projects(client: AsyncClient):
    """
    Test getting a list of projects.
    """
    response = await client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]
    assert "status" in data[0]