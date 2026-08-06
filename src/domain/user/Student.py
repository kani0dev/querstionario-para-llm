import uuid_utils as uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .Role import user_role
from .User import User


class Student(User):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    student_uuid: Mapped[str] = mapped_column(
        String,
        unique=True,
        default=lambda: str(uuid.uuid7()),
    )

    __mapper_args__ = {
        "polymorphic_identity": user_role.STUDENT,
    }
