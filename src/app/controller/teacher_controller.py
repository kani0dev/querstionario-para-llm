from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.controller.request.teacher_request import create_teacher_request
from src.app.controller.response.teacher_response import teacher_response
from src.app.service.teacher_service import teacher_service
from src.domain.user.Role import user_role
from src.domain.user.User import User
from src.infra.db.session import get_session
from src.infra.security.auth_dependency import require_role
from src.infra.security.securityService import securityService

router = APIRouter(prefix='/teacher', tags=['teacher'])
service = teacher_service()


@router.get('', response_model=list[teacher_response])
def list_teachers(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(user_role.ADMIN)),
):
    return service.get_all(session)


@router.get('/{teacher_id}', response_model=teacher_response)
def get_teacher_by_id(
    teacher_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(user_role.ADMIN)),
):
    try:
        return service.get_by_id(teacher_id, session)
    except ValueError:
        raise HTTPException(404, "teacher not found")


@router.post('', status_code=201)
def create_teacher(
    payload: create_teacher_request,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(user_role.ADMIN)),
):
    if payload.password != payload.confirm_password:
        raise HTTPException(422, "senhas não conferem")

    service = securityService(session)
    try:
        token = service.create_teacher(payload.name, payload.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(409, str(e))
