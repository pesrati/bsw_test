from sqlalchemy import CheckConstraint, Column, Integer, Numeric, String

from app.database import Base


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    coefficient = Column(Numeric(10, 2), CheckConstraint("stake>0"), nullable=False)
    deadline = Column(Integer)
    state = Column(String, index=True)
