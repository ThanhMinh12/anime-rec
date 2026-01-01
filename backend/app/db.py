from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
from typing import Generator

try:
    load_dotenv()
except Exception:
    pass

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("No DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
