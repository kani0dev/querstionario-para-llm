from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.db import Base

from .Role import user_role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100))

    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    role: Mapped[user_role] = mapped_column(Enum(user_role), default=user_role.STUDENT)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __mapper_args__ = {
        "polymorphic_on": "role",
        "polymorphic_identity": user_role.ADMIN
    }
