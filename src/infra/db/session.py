from sqlalchemy.orm import sessionmaker

from src.infra.db.db import get_conection

engine = get_conection()
SessionLocal = sessionmaker(bind=engine) if engine else None


def get_session():
    if SessionLocal is None:
        raise RuntimeError("Banco de dados não configurado: DATABASE_URL não definida.")
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
