from collections.abc import Callable
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.parcels import ParcelsRepository
from src.repository.parcels_types import ParcelsTypesRepository


class DBManager:
    """
    Database manager.

    Provides access to repositories and manages database session.
    Supports async context manager for automatic session closure.
    """

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.parcels = ParcelsRepository(self.session)
        self.types = ParcelsTypesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    def __repr__(self):
        return "DBManager"
