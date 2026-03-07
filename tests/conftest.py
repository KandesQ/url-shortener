import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from testcontainers.postgres import PostgresContainer

from core.config import settings

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer(
            f"postgres:{settings.POSTGRES_VERSION}",
            dbname="url_shortener_test"
    ) as postgres:
        settings.POSTGRES_DB = postgres.dbname
        settings.POSTGRES_USER = postgres.username
        settings.POSTGRES_PASSWORD = postgres.password
        settings.POSTGRES_HOST = postgres.get_container_host_ip()
        settings.POSTGRES_PORT = postgres.get_exposed_port(5432)

        yield postgres

@pytest_asyncio.fixture
async def async_session_local(postgres_container):
    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_session_maker

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(async_session_local):
    async with async_session_local() as db_session:
        yield db_session
        await db_session.rollback()
