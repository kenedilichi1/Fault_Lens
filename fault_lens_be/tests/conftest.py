from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.db.dependency import get_db
from app.main import app
from tests.container import postgres
from app.auth.dependencies import get_current_user
from app.users.models import User


#
# Container
#
@pytest.fixture(scope="session", autouse=True)
def postgres_container():
    postgres.start()
    yield postgres
    postgres.stop()


#
# Engine
#
@pytest.fixture(scope="session")
async def engine(postgres_container) -> AsyncGenerator[AsyncEngine, None]:

    database_url = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2://",
        "postgresql+asyncpg://",
    )

    engine = create_async_engine(
        database_url,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


#
# Connection per test
#
@pytest_asyncio.fixture(loop_scope="session")
async def connection(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncConnection, None]:

    async with engine.connect() as conn:
        transaction = await conn.begin()

        yield conn

        await transaction.rollback()


#
# Session per test
#
@pytest_asyncio.fixture(loop_scope="session")
async def db_session(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:

    Session = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
    )

    async with Session() as session:
        yield session


#
# FastAPI dependency override
#
@pytest_asyncio.fixture(loop_scope="session")
async def client(db_session: AsyncSession):
    print(id(db_session))

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def current_user(db_session: AsyncSession):
    user = User(
        email="owner@example.com",
        full_name="Organization Owner",
        password_hash="test-password-hash",
    )

    db_session.add(user)
    await db_session.flush()

    async def override_get_current_user():
        return user

    app.dependency_overrides[get_current_user] = override_get_current_user

    yield user

    app.dependency_overrides.pop(get_current_user, None)