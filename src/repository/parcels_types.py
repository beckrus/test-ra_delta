import logging
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.parcels_type import ParcelTypeAddDTO, ParcelTypeDTO
from src.models.parcels_types import ParcelTypesOrm


class ParcelsTypesRepository:
    model = ParcelTypesOrm

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[ParcelTypeDTO]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return [
            ParcelTypeDTO.model_validate(n, from_attributes=True) for n in result.scalars().all()
        ]

    async def get_by_name(self, name) -> ParcelTypeDTO:
        query = select(self.model).filter_by(name=name)
        result = await self.session.execute(query)
        return ParcelTypeDTO.model_validate(result.scalars().one(), from_attributes=True)

    async def add(self, data: ParcelTypeAddDTO) -> ParcelTypeDTO:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return ParcelTypeDTO.model_validate(result.scalars().one(), from_attributes=True)
