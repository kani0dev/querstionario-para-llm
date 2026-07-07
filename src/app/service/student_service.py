from sqlalchemy.orm import Session
from sqlalchemy import select
from src.app.controller.request.student_request import update_student
from src.domain.user.Student import Student
from src.domain.user.User import User
from src.domain.user.Role import user_role


class student_service:
    def get_all(self, session: Session) -> list[Student]:
        return session.query(Student).filter(User.role == user_role.STUDENT).all()

    def get_by_id(self, student_id: str, session: Session) -> Student:
        select_by_id_query = select(Student).where(Student.student_uuid == student_id)
        this_student = session.execute(select_by_id_query).scalar_one_or_none()
        if not this_student:
            raise ValueError("student not found")
        return this_student