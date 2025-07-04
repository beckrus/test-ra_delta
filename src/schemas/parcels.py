import uuid
from pydantic import BaseModel, Field, field_serializer


class RegisterParcelDTO(BaseModel):
    name: str = Field(max_length=100)
    weight: float = Field(ge=1)
    type_id: int
    cost_usd: float


class AddParcelDTO(RegisterParcelDTO):
    session_id: uuid.UUID


class ParcelIdDTO(BaseModel):
    id: int

class ResponseParcelDTO(ParcelIdDTO):
    name: str = Field(max_length=100)
    weight: float = Field(ge=1)
    type: str
    cost_usd: float
    delivery_cost: float | None = None

    @field_serializer('delivery_cost')
    def serialize_delivery_cost(self, value: float | None) -> str | float:
        if value is None:
            return "Не рассчитано"
        return value


class ParcelFiltersDTO(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    type_id: int | None = None
    has_delivery_cost: bool | None = None