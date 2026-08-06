
from pydantic import BaseModel


class update_teacher(BaseModel):
    name: str | None = None


class create_teacher_request(BaseModel):
    name: str
    password: str
    confirm_password: str
