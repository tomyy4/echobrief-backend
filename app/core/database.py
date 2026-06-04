from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends

sqlite_file_name = "echobrief.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Create the .db file and the tahbles if they do not exist when running the app"""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session