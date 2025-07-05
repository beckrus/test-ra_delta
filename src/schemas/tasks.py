from pydantic import BaseModel


class TaskResponseDTO(BaseModel):
    task_id: str


class TaskResultDTO(TaskResponseDTO):
    status: str
    error: str | None = None
    return_value: str
