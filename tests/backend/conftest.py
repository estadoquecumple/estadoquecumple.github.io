import os
from pathlib import Path
import pytest
import anyio
import httpx
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
    from services.api.main import app

    class APIClient:
        def request(self, method, url, **kwargs):
            async def send():
                transport = httpx.ASGITransport(app=app)
                async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
                    return await client.request(method, url, **kwargs)
            return anyio.run(send)

        def get(self, url, **kwargs):
            return self.request("GET", url, **kwargs)

        def post(self, url, **kwargs):
            return self.request("POST", url, **kwargs)

        def options(self, url, **kwargs):
            return self.request("OPTIONS", url, **kwargs)

    yield APIClient()
