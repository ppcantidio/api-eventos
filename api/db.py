import os

from dotenv import load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine, select

load_dotenv()

engine = create_engine(
    url=os.getenv("DATABASE_URL"),
    echo=True,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
