
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

    # Now get the tasks
    response = await client.get("/tasks/")

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    # First create a task to delete
    response = await create_task_function(client)
    task_id = response.json()["id"]
    
    # Delete the task
    delete_response = await client.delete(f"/tasks/?task_id={task_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["id"] == task_id

    # Verify the task is deleted
    get_response = await client.get("/tasks/?offset=0&limit=100")
    assert get_response.status_code == 200
    tasks = get_response.json()
    assert all(task["id"] != task_id for task in tasks)