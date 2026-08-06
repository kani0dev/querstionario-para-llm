from pydantic import BaseModel

from src.domain.user.Role import user_role


class teacher_response(BaseModel):
    id: int
    teacher_uuid: str
    name: str
    role: user_role

    model_config={
        "from_attributes": True
    }
