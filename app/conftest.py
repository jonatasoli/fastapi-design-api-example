import sys
from os.path import abspath
from os.path import dirname as d

import pytest
from alembic.config import main
from fastapi.testclient import TestClient

from config import settings
from main import create_app as app

root_dir = d(abspath(__file__))
sys.path.append(root_dir)


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture
def client():

    with TestClient(app()) as client:
        yield client
