from typing import List, Optional
from sqlmodel import Session, select
from .models import User, Anime, Review

def create_user(session: Session, username: str) -> User:
    user = User(username=username)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_name(session: Session, username: str) -> Optional[User]:
    return session.exec(select(User).where(User.username == username)).first()

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def create_anime(session: Session, **kwargs) -> Anime:
    anime = Anime(**kwargs)
    session.add(anime)
    session.commit()
    session.refresh(anime)
    return anime

def get_anime(session: Session, anime_id: int) -> Optional[Anime]:
    return session.get(Anime, anime_id)

def list_anime(session: Session, q: str | None = None, limit: int = 50, offset: int = 0) -> List[Anime]:
    stmt = select(Anime)
    if q:
        stmt = stmt.where(Anime.title.ilike(f"%{q}%"))
    return session.exec(stmt.offset(offset).limit(limit)).all()

def create_review(session: Session, user_id: int, anime_id: int, rating: int, text: str | None) -> Review:
    review = Review(user_id=user_id, anime_id=anime_id, rating=rating, text=text)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review

def get_user_ratings(session: Session, user_id: int):
    return session.exec(select(Review).where(Review.user_id == user_id)).all()

def get_all_ratings(session: Session):
    return session.exec(select(Review)).all()
