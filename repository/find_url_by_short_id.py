from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Url


async def find_url_by_short_id(short_id: str, db_session: AsyncSession) -> Optional[Url]:
    """
    Find Url by short identifier

    :param short_id: short identifier 
    :param db_session: async database session
    :return: None if url doesn't exist, else Url model 
    """""
    st = select(Url).where(Url.short_identifier == short_id)
    return (await db_session.execute(st)).scalar()
