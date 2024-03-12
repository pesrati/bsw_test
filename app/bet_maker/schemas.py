from pydantic import BaseModel, condecimal


class SBets(BaseModel):
    event_id: int
    amount: condecimal(decimal_places=2, gt=0)  # type: ignore
