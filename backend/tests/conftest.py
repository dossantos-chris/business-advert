import os
import sys
sys.path.append(os.getcwd()) 

from httpx import AsyncClient
import pytest

from app.server.app import app

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def test_client():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac