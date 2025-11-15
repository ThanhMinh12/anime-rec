from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import get_session
from ..models import Anime, Review
from sqlalchemy import func

router = APIRouter(prefix="/anime", tags=["anime"])

@router.get("/")
def list_anime(
    q: str | None = Query(default=None, description="Search by title"),
    genre: str | None = Query(default=None, description="Filter by genre"),
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    stmt = select(Anime)

    if q:
        stmt = stmt.where(Anime.title.ilike(f"%{q}%"))

    if genre:
        stmt = stmt.where(Anime.genres.ilike(f"%{genre}%"))

    stmt = stmt.limit(limit).offset(offset)

    return session.exec(stmt).all()

@router.get("/search")
def search_anime(
    q: str = Query(..., description="Search query"),
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    stmt = (
        select(Anime)
        .where(Anime.title.ilike(f"%{q}%"))
        .offset(offset)
        .limit(limit)
    )
    results = session.exec(stmt).all()

    return {
        "query": q,
        "results": results,
        "count": len(results),
    }

@router.get("/genre/{genre}")
def get_by_genre(
    genre: str,
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    stmt = (
        select(Anime)
        .where(Anime.genres.ilike(f"%{genre}%"))
        .limit(limit)
        .offset(offset)
    )
    return session.exec(stmt).all()

@router.get("/genres")
def list_genres(session: Session = Depends(get_session)):
    stmt = select(Anime.genres)
    rows = session.exec(stmt).all()

    genre_set = set()
    for row in rows:
        if row:
            for g in row.split(","):
                genre_set.add(g.strip())

    return sorted(genre_set)

@router.get("/random")
def random_anime(session: Session = Depends(get_session)):
    stmt = select(Anime).order_by(func.random()).limit(1)
    return session.exec(stmt).first()


@router.get("/trending")
def trending(session: Session = Depends(get_session), limit: int = 20):
    stmt = (
        select(
            Anime,
            func.count(Review.id).label("review_count")
        )
        .join(Review, Review.anime_id == Anime.id)
        .group_by(Anime.id)
        .order_by(func.count(Review.id).desc())
        .limit(limit)
    )

    rows = session.exec(stmt).all()

    return [
        {"anime": anime, "reviews": count}
        for anime, count in rows
    ]

@router.get("/{anime_id}")
def get_anime(anime_id: int, session: Session = Depends(get_session)):
    anime = session.get(Anime, anime_id)
    if not anime:
        return {"error": "Anime not found"}
    return anime