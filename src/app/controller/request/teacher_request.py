from pydantic import BaseModel
from typing import Optional


class update_teacher(BaseModel):
    name: Optional[str] = None


class create_teacher_request(BaseModel):
    name: str
    password: str
    confirm_password: str