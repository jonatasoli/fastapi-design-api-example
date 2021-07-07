import sys
from os.path import abspath
from os.path import dirname as d

import pytest
import asyncio
# import alembic.config
from fastapi.testclient import TestClient

from config import settings
from ext.db.database import get_engine_main
from ext.db.base_class import BaseModel
from sqlalchemy.orm import declarative_base
from main import create_app as app
root_dir = d(abspath(__file__))
sys.path.append(root_dir)

meta = BaseModel.metadata


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope="session")
async def apply_migrations() -> None:
    engine = get_engine_main()
    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture
def client():
    with TestClient(app()) as client:
        yield client
