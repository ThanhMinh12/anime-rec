from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
from app.models import User, Manga, Review  

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not in .env")

engine = create_engine(DATABASE_URL, echo=False)
def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    init_db()
    print("Tables done")
