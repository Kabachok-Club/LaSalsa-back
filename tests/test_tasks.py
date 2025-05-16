
import pytest
from httpx import AsyncClient


def create_task_function(client: AsyncClient):
    return client.post("/tasks/", json={
        "name": "Test Task",
        "description": "Created via test",
        "status": "TODO"
    })

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await create_task_function(client)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Task"

@pytest.mark.asyncio
async def test_get_tasks(client: AsyncClient):
    # First create a task to get
    await create_task_function(client)
    await create_task_function(client)
    await create_task_function(client)
    response = await client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3