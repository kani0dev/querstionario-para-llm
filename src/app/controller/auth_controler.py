from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from jwt import PyJWTError
from src.infra.db.session import get_session
from src.infra.security.securityService import securityService
from src.infra.security.token.token_service import create_acess_token, decode_token
from src.domain.user.Student import Student
from src.domain.user.Teacher import Teacher
from src.domain.user.Role import user_role
from src.app.controller.request.validate_request import validate_request
from src.app.controller.response.validate_response import validate_response


class Request(BaseModel):
    username: str
    password: str



router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=201)
def signup(payload: Request, session: Session = Depends(get_session)):
    service = securityService(session)
    try:
        token = service.singup(payload.username, payload.password)
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.post("/login")
def login(payload: Request, session: Session = Depends(get_session)):
    service = securityService(session)
    user = service.authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="usuário ou senha inválidos"
        )
    if user.is_active==False:
        raise HTTPException(
            status_code=401,
            detail="usuario desativado"
        )
    token = create_acess_token(user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }