
from pydantic import BaseModel


class student_response(BaseModel):
    id: int
    student_uuid: str
    name: str

    # issso permite o fastapi a mappear a model para a response :) eu odeio magia
    model_config={
        "from_attributes": True
    }
