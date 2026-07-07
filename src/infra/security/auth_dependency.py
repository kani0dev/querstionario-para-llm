from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
from jwt import PyJWTError

from src.infra.db.session import get_session
from src.infra.security.token.token_service import decode_token
from src.domain.user.User import User
from src.domain.user.Student import Student
from src.domain.user.Teacher import Teacher
from src.domain.user.Role import user_role

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        role_value = payload.get("role")
    except PyJWTError:
        raise HTTPException(401, "invalid token")

    if not sub or not role_value:
        raise HTTPException(401, "invalid token")

    try:
        role = user_role(role_value)
    except ValueError:
        raise HTTPException(401, "invalid token")

    if role == user_role.ADMIN:
        user = session.get(User, int(sub))
    else:
        model_class = Teacher if role == user_role.TEACHER else Student
        uuid_column = Teacher.teacher_uuid if role == user_role.TEACHER else Student.student_uuid
        stmt = select(model_class).where(uuid_column == sub)
        user = session.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(401, "user not found")

    return user


def require_role(*roles: user_role):
    async def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(403, "insufficient permissions")
        return user
    return role_checker
