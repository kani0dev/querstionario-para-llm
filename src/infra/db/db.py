import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_USER = os.getenv("DB_USER", "quiz2llm")
DB_PASS = os.getenv("DB_PASS", "quiz2llm_pass")
HOST = os.getenv("HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "quiz2llm")


def get_database_url():
    explicit = os.getenv("DATABASE_URL")
    if explicit:
        return explicit
    return f"mysql+pymysql://{DB_USER}:{DB_PASS}@{HOST}:{DB_PORT}/{DB_NAME}"

print(get_database_url())
def get_conection():
    try:
        engine = create_engine(get_database_url())
        return engine
    except Exception as e:
        print('erro ao conectar ao servido \n', e)
        return e


class Base(DeclarativeBase):
    pass
