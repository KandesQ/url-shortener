from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Url



async def find_url(original_url: str, db_session: AsyncSession) -> Optional[Url]:
    """
    Finds the url from the original url. If url doesn't exist, returns None

    :param original_url: original url string
    :param db_session: async database session
    :return: None if url doesn't exist, else Url model
    """
    st = select(Url).where(Url.original_url == original_url)
    return (await db_session.execute(st)).scalar()
