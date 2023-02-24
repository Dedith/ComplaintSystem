from pydantic import BaseModel
from typing import Literal
from models.enums import State


class ComplaintIn(BaseModel):

    title: str
    description: str
    photo_url: str
    amount: float
    status: Literal[State.pending] = State.pending
