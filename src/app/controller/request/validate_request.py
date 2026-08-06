
from pydantic import BaseModel


class validate_request(BaseModel):
    token: str
    required_role: int | None = None
