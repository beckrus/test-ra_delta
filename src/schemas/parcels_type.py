from pydantic import BaseModel


class ParcelTypeDTO(BaseModel):
    id: int
    name: str


class ParcelTypeAddDTO(BaseModel):
    name: str
