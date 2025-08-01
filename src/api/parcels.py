from fastapi import APIRouter, Query, Response

from src.exceptions import (
    FKObjectNotFoundException,
    ParcelAlreadyAssignedException,
    ParcelAlreadyAssignedHTTPException,
    ParcelNotFoundException,
    ParcelNotFoundHTTPException,
    SessionNotFoundException,
    SessionNotFoundHTTPException,
    TypeNotFoundHTTPException,
)
from src.schemas.parcels import (
    AssignTransportResponseDTO,
    ParcelFiltersDTO,
    RegisterParcelDTO,
    ParcelIdDTO,
    ResponseParcelDTO,
)
from src.api.dependencies import DBDep, SessionIdDep, create_session_id


router = APIRouter(prefix="/parcels", tags=["Parcels"])


@router.post(
    "",
    summary="Register a new parcel",
    description="Register a new parcel with the provided details. The weight should be specified in grams.",
)
async def register_parcel(
    data: RegisterParcelDTO, db: DBDep, session_id: SessionIdDep, response: Response
) -> ParcelIdDTO:
    try:
        if not session_id:
            session_id = create_session_id()
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
            )
        result = await db.parcels.add(data, session_id)
        await db.commit()
        return result
    except FKObjectNotFoundException:
        raise TypeNotFoundHTTPException
    except SessionNotFoundException as e:
        raise SessionNotFoundHTTPException from e


@router.get(
    "",
    summary="Get all parcels for the current session",
    description="Retrieve a list of all parcels registered by the current session.",
)
async def get_my_parcels(
    db: DBDep,
    session_id: SessionIdDep,
    limit: int = Query(default=10, ge=1, le=100, description="Number of records (1-100)"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    type_id: int | None = Query(default=None, description="Filter by parcel type id"),
    has_delivery_cost: bool | None = Query(
        default=None, description="Filter by presence of delivery cost"
    ),
) -> list[ResponseParcelDTO]:
    filters = ParcelFiltersDTO(
        limit=limit, offset=offset, type_id=type_id, has_delivery_cost=has_delivery_cost
    )

    return await db.parcels.get_all(session_id, filters)


@router.get(
    "/{parcel_id}",
    summary="Get parcel by id for the current session",
    description="Retrieve a parcel registered by the current session.",
)
async def get_my_parcel_by_id(
    parcel_id: int, db: DBDep, session_id: SessionIdDep
) -> ResponseParcelDTO:
    try:
        return await db.parcels.get_by_id(parcel_id=parcel_id, session_id=session_id)
    except ParcelNotFoundException as e:
        raise ParcelNotFoundHTTPException from e


@router.post(
    "/{parcel_id}/assign-transport",
    summary="Assign parcel to transport company",
    description="Atomically assigns a parcel to a transport company with race condition protection",
)
async def assign_transport_company(
    parcel_id: int, transport_company_id: int, db: DBDep
) -> AssignTransportResponseDTO:
    try:
        result = await db.parcels.assign_transport_company(
            parcel_id=parcel_id, transport_company_id=transport_company_id
        )
        await db.commit()
        return result
    except ParcelNotFoundException:
        raise ParcelNotFoundHTTPException
    except ParcelAlreadyAssignedException:
        raise ParcelAlreadyAssignedHTTPException
