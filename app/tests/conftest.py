import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from app.bet_maker.models import Bets
from app.config import settings
from app.database import Base, async_session_maker, engine
import json
from app.line_provider.router import app as app_line
from app.bet_maker.router import app as app_bet

from app.line_provider.models import Events




@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)
        
    bets = open_mock_json("bets")   
    events = open_mock_json("events")

    async with async_session_maker() as session:
        add_events = insert(Events).values(events)
        add_bets = insert(Bets).values(bets)

        await session.execute(add_events)
        await session.execute(add_bets)

        await session.commit()


@pytest.mark.asyncio(scope="module")
async def test_find(connection):
    pass


@pytest.fixture(scope="function")
async def ac_line():
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app_line), base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture(scope="session")
async def ac_bet():
    async with AsyncClient(
        transport = httpx.ASGITransport(app=app_bet), base_url="http://test"
    ) as ac:
        yield ac
    