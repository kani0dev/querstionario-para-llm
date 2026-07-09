from sqlalchemy.orm import Session
from src.domain.user.User import User
from src.domain.user.Student import Student
from src.domain.user.Teacher import Teacher
from src.domain.user.Role import user_role
from src.infra.security.securitModel import user_credentials
from src.infra.security.securityConfig import password_encoder
from src.infra.security.token import token_service

from datetime import datetime, timezone


class securityService:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        user = self.session.query(User).filter(User.name == username).first()
        return user

    def verify_password(self, username: str, password: str) -> bool:
        user = self.get_by_username(username)
        if not user:
            return False

        creds = self.session.get(user_credentials, user.id)
        if not creds:
            return False

        return password_encoder.verify_password(password, creds.password)

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.get_by_username(username)
        if not user:
            return None

        creds = self.session.get(user_credentials, user.id)
        if not creds:
            return None

        if not password_encoder.verify_password(password, creds.password):
            return None

        return user

    def singup(self, username: str, password: str) -> str:
        user = self.get_by_username(username)
        if user:
            raise ValueError("usuário já existe")

        new_user = Student(name=username)
        self.session.add(new_user)
        # o flush serve para ''''pegar'''' um novo id.
        self.session.flush()
        hashed = password_encoder.hash_password(password)

        creds = user_credentials(
            user_id=new_user.id,
            password=hashed,
            last_password_change=datetime(1970,1,1,  tzinfo=timezone.utc),
            fail_attempts=0,
        )
        self.session.add(creds)
        self.session.commit()
        token = token_service.create_acess_token(new_user)

        return token

    def create_teacher(self, name: str, password: str) -> str:
        user = self.get_by_username(name)
        if user:
            raise ValueError("usuário já existe")

        new_teacher = Teacher(name=name)
        self.session.add(new_teacher)
        self.session.flush()
        hashed = password_encoder.hash_password(password)

        creds = user_credentials(
            user_id=new_teacher.id,
            password=hashed,
            last_password_change=datetime(1970, 1, 1, tzinfo=timezone.utc),
            fail_attempts=0,
        )
        self.session.add(creds)
        self.session.commit()
        token = token_service.create_acess_token(new_teacher)

        return token

    def signup_teacher(self, username: str, password: str) -> str:
        user = self.get_by_username(username)
        if user:
            raise ValueError("usuário já existe")

        new_user = Teacher(name=username)
        self.session.add(new_user)
        self.session.flush()
        hashed = password_encoder.hash_password(password)

        creds = user_credentials(
            user_id=new_user.id,
            password=hashed,
            last_password_change=datetime(1970, 1, 1, tzinfo=timezone.utc),
            fail_attempts=0,
        )
        self.session.add(creds)
        self.session.commit()
        token = token_service.create_acess_token(new_user)

        return token
    