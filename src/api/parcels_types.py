from fastapi import APIRouter

from src.schemas.parcels_type import ParcelTypeDTO
from src.api.dependencies import DBDep


router = APIRouter(prefix="/parcel_types", tags=["Parcel Types"])


@router.get(
    "",
    summary="Get all parcel types",
    description="Retrieve a list of all parcel types",
)
async def get_parcel_types(db: DBDep) -> list[ParcelTypeDTO]:
    return await db.types.get_all()
