from fastapi import APIRouter
from taskiq_redis.exceptions import ResultIsMissingError

from src.schemas.tasks import TaskResponseDTO, TaskResultDTO
from src.exceptions import TaskNotFoundHTTPException
from src.tasks.task_delivery_calc import calculate_delivery_cost_for_parcel
from src.tasks.taskiq import broker


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/update-costs")
async def update_parcels_delivery_cost() -> TaskResponseDTO:
    task = await calculate_delivery_cost_for_parcel.kiq()
    task_id = task.task_id
    return TaskResponseDTO(task_id=task_id)


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str) -> TaskResultDTO:
    try:
        result = await broker.result_backend.get_result(task_id)
        return TaskResultDTO(
            task_id=task_id,
            status="failed" if result.is_err else "succcess",
            error=str(result.error) if result.is_err else None,
            return_value=str(result.return_value),
        )
    except (ResultIsMissingError, KeyError):
        raise TaskNotFoundHTTPException
