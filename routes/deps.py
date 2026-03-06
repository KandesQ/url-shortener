from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Annotated, AsyncGenerator

from core.db import async_engine

async_db_sessionmaker = async_sessionmaker(
    async_engine,
    expire_on_commit=False
)

async def get_db_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_db_sessionmaker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db_async_session)]
