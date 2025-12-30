from typing import List, Optional
from sqlmodel import Session, select
from .models import User, Manga, Review

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

def create_manga(session: Session, **kwargs) -> Manga:
    manga = Manga(**kwargs)
    session.add(manga)
    session.commit()
    session.refresh(manga)
    return manga

def get_manga(session: Session, manga_id: int) -> Optional[Manga]:
    return session.get(Manga, manga_id)

def list_manga(session: Session, q: str | None = None, limit: int = 50, offset: int = 0) -> List[Manga]:
    stmt = select(Manga)
    if q:
        stmt = stmt.where(Manga.title.ilike(f"%{q}%"))
    return session.exec(stmt.offset(offset).limit(limit)).all()

def create_review(session: Session, user_id: int, manga_id: int, rating: int, text: str | None) -> Review:
    review = Review(user_id=user_id, manga_id=manga_id, rating=rating, text=text)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review

def get_user_ratings(session: Session, user_id: int):
    return session.exec(select(Review).where(Review.user_id == user_id)).all()

def get_all_ratings(session: Session):
    return session.exec(select(Review)).all()
