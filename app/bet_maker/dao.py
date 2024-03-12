from pydantic import BaseModel
from sqlalchemy import select

from app.bet_maker.models import Bets
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.line_provider.models import Events


class Event(BaseModel):
    id: int
    state: str


class BetsDAO(BaseDAO):
    model = Bets

    @classmethod
    async def join_bets_with_events(cls):
        async with async_session_maker() as session:
            stmt = select(Events).join(Bets, Bets.event_id == Events.id)
            result = await session.execute(stmt)
            events = result.scalars().all()
            return [Event(id=event.id, state=event.state) for event in events]
