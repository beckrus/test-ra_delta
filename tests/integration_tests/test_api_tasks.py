from unittest.mock import AsyncMock, patch
from httpx import AsyncClient


async def test_api_update_costs(ac: AsyncClient):
    response = await ac.post("/tasks/update-costs")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data


async def test_api_task_status(ac: AsyncClient):
    with patch("src.api.tasks.broker.result_backend.get_result") as mock_get_result:
        mock_result = AsyncMock()
        mock_result.is_err = False
        mock_result.error = None
        mock_result.return_value = True
        mock_get_result.return_value = mock_result

        # test
        response = await ac.post("/tasks/update-costs")
        assert response.status_code == 200
        task_data = response.json()
        task_id = task_data["task_id"]

        status_response = await ac.get(f"/tasks/task-status/{task_id}")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert "status" in status_data
        assert "task_id" in status_data


async def test_api_task_not_found(ac: AsyncClient):
    response = await ac.get("/tasks/task-status/nonexistent-task-id")
    assert response.status_code == 404
