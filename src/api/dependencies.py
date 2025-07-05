from typing import Annotated, Any, AsyncGenerator
import uuid

from fastapi import Depends, Request

from src.database import async_session_maker, async_session_maker_null_pool
from src.utils.db_manager import DBManager


def get_db_manager_null_pull() -> DBManager:
    return DBManager(session_factory=async_session_maker_null_pool)


def get_db_manager() -> DBManager:
    return DBManager(session_factory=async_session_maker)


async def get_db() -> AsyncGenerator[DBManager, Any]:
    async with get_db_manager() as db:
        yield db


def create_session_id() -> str:
    return str(uuid.uuid4())


def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    return session_id


DBDep = Annotated[DBManager, Depends(get_db)]

SessionIdDep = Annotated[str, Depends(get_session_id)]
