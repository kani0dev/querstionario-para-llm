from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.controller.response.student_response import student_response
from src.app.service.student_service import student_service
from src.domain.user.User import User
from src.infra.db.session import get_session
from src.infra.security.auth_dependency import get_current_user

router = APIRouter(prefix='/student', tags=['student'])
service = student_service()


@router.get('', response_model=list[student_response])
def list_students(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return service.get_all(session)


@router.get('/{student_id}', response_model=student_response)
def get_student_by_id(
    student_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.get_by_id(student_id, session)
    except ValueError:
        raise HTTPException(404, 'Student not found')
