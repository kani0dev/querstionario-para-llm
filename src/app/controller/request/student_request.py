
from pydantic import BaseModel


class update_student(BaseModel):
    name: str | None = None
