# ruff: noqa: E402
import pytest

from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient
from schemas.parcels_type import ParcelTypeAddDTO
from src.api.dependencies import get_db, get_db_manager_null_pull
from src.database import engine_null_pool, Base
from src.models import *  # noqa: F403
from src.config import settings
from src.main import app
from src.utils.db_manager import DBManager


@pytest.fixture(autouse=True, scope="session")
async def check_mode() -> None:
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> AsyncGenerator[DBManager, Any]:
    async with get_db_manager_null_pull() as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, Any]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture()
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with get_db_manager_null_pull() as db:
        types = ["одежда", "электроника", "разное"]
        for t in types:
            await db.types.add(ParcelTypeAddDTO(name=t))
        await db.commit()
