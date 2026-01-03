from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)


"""class Anime(SQLModel, table=True):
    __tablename__ = "anime"

    id: Optional[int] = Field(default=None, primary_key=True)
    jikan_id: Optional[int] = Field(default=None, index=True, unique=True)
    title: str = Field(index=True)
    synopsis: Optional[str] = None
    image_url: Optional[str] = None
    year: Optional[int] = None
    score: Optional[float] = None
    genres: Optional[str] = None
    author: Optional[str] = None
    studio: Optional[str] = None"""


class Manga(SQLModel, table=True):
    __tablename__ = "manga"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    synopsis: Optional[str] = None
    year: Optional[int] = None
    score: Optional[float] = None
    genres: Optional[str] = None
    author: Optional[str] = None
    illustrator: Optional[str] = None
    publisher: Optional[str] = None
    magazine: Optional[str] = None
    chapters: Optional[int] = None
    volumes: Optional[int] = None


class Review(SQLModel, table=True):
    __tablename__ = "review"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    manga_id: int = Field(foreign_key="manga.id")
    rating: int = Field(ge=1, le=10)
    text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)



class Genre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

class MangaGenre(SQLModel, table=True):
    manga_id: int = Field(foreign_key="manga.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)