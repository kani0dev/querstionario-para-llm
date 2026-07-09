from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.infra.db.session import get_session
from src.infra.security.securityService import securityService
from src.infra.security.token.token_service import create_acess_token
from src.infra.wordle.wordle_service import get_daily_word


class Request(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup/teacher", status_code=201)
def signup_teacher(
    payload: Request,
    secret_word: str,
    session: Session = Depends(get_session),
):
    daily_word = get_daily_word()
    if daily_word is None:
        raise HTTPException(503, "não foi possível validar a palavra mágica")
    if secret_word.lower() != daily_word.lower():
        raise HTTPException(403, "palavra mágica inválida")

    service = securityService(session)
    try:
        token = service.signup_teacher(payload.username, payload.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.post("/signup", status_code=201)
def signup(payload: Request, session: Session = Depends(get_session)):
    service = securityService(session)
    try:
        token = service.singup(payload.username, payload.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.post("/login")
def login(payload: Request, session: Session = Depends(get_session)):
    service = securityService(session)
    user = service.authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="usuário ou senha inválidos")

    token = create_acess_token(user)

    return {"access_token": token, "token_type": "bearer"}
