from sqlalchemy.ext.asyncio import create_async_engine

from core.config import settings

async_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
