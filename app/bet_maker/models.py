from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class Bets(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    amount = Column(Numeric(10, 2), CheckConstraint("stake>0"), nullable=False)

    event = relationship("Events", backref="bets")
