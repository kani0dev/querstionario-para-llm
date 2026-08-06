import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_database_url():
    return DATABASE_URL


def get_conection():
    if not get_database_url():
        print("DATABASE_URL não definida. Nenhuma conexão será realizada.")
        return None
    try:
        engine = create_engine(get_database_url())
        return engine
    except Exception as e:
        print('erro ao conectar ao servidor \n', e)
        return e


class Base(DeclarativeBase):
    pass
