from sqlalchemy import update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.line_provider.models import Events


class EventsDAO(BaseDAO):
    model = Events

    @classmethod
    async def update(cls, **data):
        async with async_session_maker() as session:
            query = update(cls.model).values(**data).where(cls.model.id == data["id"])
            await session.execute(query)
            await session.commit()
