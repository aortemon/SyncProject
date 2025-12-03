import os
import shutil
import sys
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_db_url
from app.entities.admin.db_dumper import DatabaseUtils
from app.main import app
from database.session import Sessioner


@pytest_asyncio.fixture(scope="module", autouse=True)
async def set_test_database():
    DATABASE_URL = get_db_url(is_test=True)
    engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

    async with engine.begin() as conn:
        inspector = await conn.run_sync(lambda sync_conn: inspect(sync_conn))
        tables = await conn.run_sync(lambda sync_conn: inspector.get_table_names())

        for table in tables:
            if not table.startswith("alembic_"):
                await conn.execute(text(f'TRUNCATE TABLE "{table}" CASCADE;'))

    Sessioner.session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        with open("tests/db_test_init.sql", mode="r", encoding="utf-8") as f:
            init_query = "".join(f.readlines())
        init_queries = [x + ";" for x in init_query.split(";")]

        for query in init_queries:
            await conn.execute(text(query))

    yield
    

@pytest_asyncio.fixture
async def setup_test_db_dumper():
    path = Path.home() / "SyncProject" / "tests" / "backups"
    os.makedirs(path, exist_ok=True)
    DatabaseUtils.setup_test()
    yield
    shutil.rmtree(path)


@pytest_asyncio.fixture
async def auto_async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


async def generate_client_logged_in_as(username, password) -> AsyncClient:
    client: AsyncClient = AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )

    response = await client.post(
        url="/auth/login/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"username": username, "password": password},
    )

    assert response.status_code == 200
    auth_data = response.json()
    client.headers["Authorization"] = (
        f"{auth_data['token_type']} {auth_data['access_token']}"
    )

    return client


@pytest_asyncio.fixture
async def async_client_as_admin():
    client = await generate_client_logged_in_as("admin@admin.admin", "temikadmin")
    yield client


@pytest_asyncio.fixture
async def async_client_as_manager():
    client = await generate_client_logged_in_as("manager@manager.manager", "temikadmin")
    yield client


@pytest_asyncio.fixture
async def async_client_as_executor():
    client = await generate_client_logged_in_as("exec@exec.exec", "temikadmin")
    yield client
