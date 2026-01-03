import re
from sqlmodel import Session, create_engine, select
from app.models import Manga, Genre, MangaGenre
from dotenv import load_dotenv
import os
from sqlalchemy.dialects.postgresql import insert

try:
    load_dotenv()
except Exception:
    pass

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("No DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def parse_genres(raw: str) -> list[str]:
    if not raw:
        return []
    cleaned = re.sub(r"\[\s*\d+\s*\]", "", raw)

    parts = re.split(r"\s{2,}", cleaned)

    return [p.strip() for p in parts if p.strip()]

with Session(engine) as session:
    mangas = session.exec(select(Manga)).all()
    genre_cache: dict[str, int] = {}

    genre_cache = {}

    for manga in mangas:
        genres = parse_genres(manga.genres)

        for g in genres:
            if g not in genre_cache:
                genre = session.exec(
                    select(Genre).where(Genre.name == g)
                ).first()

                if not genre:
                    genre = Genre(name=g)
                    session.add(genre)
                    session.commit()
                    session.refresh(genre)

                genre_cache[g] = genre.id
            stmt = insert(MangaGenre).values(manga.id, genre_cache[g]).on_conflict_do_nothing()

            session.exec(stmt)

    session.commit()
