import os

from dotenv import load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine, select

load_dotenv()
connect_args = {"check_same_thread": False}
engine = create_engine(
    url=os.getenv("DATABASE_URL"),
    echo=True,
    connect_args=connect_args,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
