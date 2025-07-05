import logging
from sqlalchemy import and_, insert, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repository.utils import get_missing_fk
from src.exceptions import (
    FKObjectNotFoundException,
    ParcelAlreadyAssignedException,
    ParcelNotFoundException,
)
from src.schemas.parcels import (
    AddParcelDTO,
    ParcelFiltersDTO,
    ParcelIdDTO,
    ParcelUpdateCostDTO,
    RegisterParcelDTO,
    ResponseParcelDTO,
)
from src.models.parcels import ParcelsOrm


class ParcelsRepository:
    model = ParcelsOrm

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: RegisterParcelDTO, session_id: str) -> ParcelIdDTO:
        try:
            parcel_data = data.model_dump()
            parcel_data["session_id"] = session_id
            parcel_data = AddParcelDTO.model_validate(parcel_data)
            stmt = insert(self.model).values(**parcel_data.model_dump())
            result = await self.session.execute(stmt)
            inserted_id = result.lastrowid
            return ParcelIdDTO(id=inserted_id)
        except IntegrityError as e:
            logging.error(
                f"Can't add data in DB, error type: {type(e.orig.__cause__)=}, input {data=}"
            )
            if e.orig.args[0] == 1452:
                key = get_missing_fk(str(e))
                logging.error(f"Missing FOREIGN KEY: {key}")
                raise FKObjectNotFoundException from e
            raise e

    async def get_all(self, session_id: str, filters: ParcelFiltersDTO) -> list[ResponseParcelDTO]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.type))
            .filter_by(session_id=session_id)
        )

        conditions = []
        if filters.type_id is not None:
            conditions.append(self.model.type_id == filters.type_id)
        if filters.has_delivery_cost is not None:
            if filters.has_delivery_cost:
                conditions.append(self.model.delivery_cost.is_not(None))
            else:
                conditions.append(self.model.delivery_cost.is_(None))
        if conditions:
            stmt = stmt.filter(and_(*conditions))

        stmt = stmt.order_by(self.model.id).offset(filters.offset).limit(filters.limit)

        result = await self.session.execute(stmt)

        rows = result.scalars().all()

        items = []

        for parcel in rows:
            items.append(
                ResponseParcelDTO(
                    id=parcel.id,
                    name=parcel.name,
                    weight=parcel.weight,
                    type=parcel.type.name,
                    cost_usd=parcel.cost_usd,
                    delivery_cost=parcel.delivery_cost,
                )
            )

        return items

    async def get_by_id(self, parcel_id: int, session_id: str) -> ResponseParcelDTO:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.type))
            .filter_by(session_id=session_id, id=parcel_id)
        )
        result = await self.session.execute(stmt)
        parcel = result.scalars().one_or_none()
        if not parcel:
            raise ParcelNotFoundException
        return ResponseParcelDTO(
            id=parcel.id,
            name=parcel.name,
            weight=parcel.weight,
            type=parcel.type.name,
            cost_usd=parcel.cost_usd,
        )

    async def get_by_id_wo_session(self, parcel_id: int) -> ResponseParcelDTO:
        stmt = select(self.model).options(selectinload(self.model.type)).filter_by(id=parcel_id)
        result = await self.session.execute(stmt)
        parcel = result.scalars().one_or_none()
        if not parcel:
            raise ParcelNotFoundException
        return ResponseParcelDTO(
            id=parcel.id,
            name=parcel.name,
            weight=parcel.weight,
            type=parcel.type.name,
            cost_usd=parcel.cost_usd,
        )

    async def update_delivery_cost(self, parcel_id: int, delivery_cost: float) -> None:
        stmt = (
            update(self.model).filter_by(id=parcel_id).values(delivery_cost=round(delivery_cost, 2))
        )
        await self.session.execute(stmt)

    async def assign_transport_company(self, parcel_id: int, transport_company_id: int) -> bool:
        stmt = select(self.model).filter_by(id=parcel_id).with_for_update()
        result = await self.session.execute(stmt)
        parcel = result.scalars().one_or_none()
        if not parcel:
            raise ParcelNotFoundException
        if parcel.transport_company_id is not None:
            raise ParcelAlreadyAssignedException
        update_stmt = (
            update(self.model)
            .filter_by(id=parcel_id)
            .values(transport_company_id=transport_company_id)
        )
        await self.session.execute(update_stmt)

        return True

    async def update_delivery_cost_batch(self, delivery_costs: list[ParcelUpdateCostDTO]) -> int:
        data = [n.model_dump() for n in delivery_costs]
        stmt = update(self.model)
        await self.session.execute(stmt, data)
        return len(data)

    async def get_without_delivery_cost(self) -> list[ResponseParcelDTO]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.type))
            .filter_by(delivery_cost=None)
            .with_for_update(skip_locked=True)
        )
        result = await self.session.execute(stmt)
        return [
            ResponseParcelDTO(
                id=parcel.id,
                name=parcel.name,
                weight=parcel.weight,
                type=parcel.type.name,
                cost_usd=parcel.cost_usd,
                delivery_cost=parcel.delivery_cost,
            )
            for parcel in result.scalars().all()
        ]
