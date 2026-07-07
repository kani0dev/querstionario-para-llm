from sqlalchemy.orm import Session
from sqlalchemy import select, insert
import uuid

from src.app.controller.request.teacher_request import update_teacher
from src.domain.user.User import User
from src.domain.user.Teacher import Teacher
from src.domain.user.Student import Student
from src.domain.user.Role import user_role


class teacher_service:
    def get_all(self, session: Session) -> list[Teacher]:
        return session.query(Teacher).filter(User.role == user_role.TEACHER).all()

    def get_by_id(self, teacher_id: str, session: Session) -> Teacher:
        select_by_id_query = select(Teacher).where(Teacher.teacher_uuid == teacher_id)
        this_teacher = session.execute(select_by_id_query).scalar_one_or_none()
        if not this_teacher:
            raise ValueError("teacher not found")
        return this_teacher
