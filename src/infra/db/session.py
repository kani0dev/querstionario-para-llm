from sqlalchemy.orm import sessionmaker

from src.infra.db.db import get_conection

engine = get_conection()
SessionLocal = sessionmaker(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
