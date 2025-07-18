import os
from asgi_lifespan import LifespanManager

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

os.environ["TEST_ENVIRONMENT"] = "true"

from main import app
from src.models import Base
from tests.utils.postgres_db import engine


@pytest_asyncio.fixture(scope="session")
async def client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            yield ac
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

