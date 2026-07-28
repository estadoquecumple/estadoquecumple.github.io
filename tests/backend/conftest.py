import os
from pathlib import Path
import pytest
from dotenv import dotenv_values
from sqlalchemy import text

if os.name == "nt":
    lab = dotenv_values(".env.lab")
    os.environ["DATABASE_URL"] = (
        f"postgresql+psycopg://{lab['POSTGRES_APP_USER']}:{lab['POSTGRES_APP_PASSWORD']}"
        f"@127.0.0.1:{lab.get('POSTGRES_PORT', '55432')}/{lab['POSTGRES_DB']}"
    )

from services.shared.db import engine

@pytest.fixture
def db():
    with engine.begin() as connection:
        yield connection

@pytest.fixture
def api():
    from fastapi.testclient import TestClient
    from services.api.main import app
    with TestClient(app) as client:
        yield client
