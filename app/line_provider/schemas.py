from typing import Optional

from pydantic import BaseModel, condecimal


class SEvent(BaseModel):
    id: int
    coefficient: condecimal(decimal_places=2, gt=0)  # type: ignore
    deadline: Optional[int] = None
    state: Optional[str] = None
