from pydantic import BaseModel
from models.enums import RoleType


class UserOut(BaseModel):

    id: int
    first_name: str
    last_name: str
    phone: str
    role: RoleType
    iban: str
