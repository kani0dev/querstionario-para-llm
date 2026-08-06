import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv

from src.domain.user.Student import Student
from src.domain.user.Teacher import Teacher
from src.domain.user.User import User

load_dotenv()

SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('JWT_ALGORITHM')
TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE', '30'))


def create_acess_token(user: User):
    expire = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)


    if isinstance(user, Student):
        sub = user.student_uuid
    elif isinstance(user, Teacher):
        sub = user.teacher_uuid
    else:
        sub = str(user.id)

    payload = {
        "sub": sub,
        "username": user.name,
        "role": user.role.value,
        "is_active": user.is_active,
        "exp": int(expire.timestamp())
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
