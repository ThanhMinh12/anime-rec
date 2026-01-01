from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import get_session
from ..models import Review, Manga
from sqlalchemy import func

router = APIRouter(prefix="/manga", tags=["manga"])

@router.get("/")
def list_manga(
    q: str | None = Query(default=None, description="Search by title"),
    genre: str | None = Query(default=None, description="Filter by genre"),
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    stmt = select(Manga)

    if q:
        stmt = stmt.where(Manga.title.ilike(f"%{q}%"))

    if genre:
        stmt = stmt.where(Manga.genres.ilike(f"%{genre}%"))

    stmt = stmt.limit(limit).offset(offset)

    return session.exec(stmt).all()

@router.get("/search")
def search_manga(
    q: str = Query(..., description="Search query"),
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    stmt = (
        select(Manga)
        .where(Manga.title.ilike(f"%{q}%"))
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
        select(Manga)
        .where(Manga.genres.ilike(f"%{genre}%"))
        .limit(limit)
        .offset(offset)
    )
    return session.exec(stmt).all()

@router.get("/genres")
def list_genres(session: Session = Depends(get_session)):
    stmt = select(Manga.genres)
    rows = session.exec(stmt).all()

    genre_set = set()
    for row in rows:
        if row:
            for g in row.split(","):
                genre_set.add(g.strip())

    return sorted(genre_set)

@router.get("/random")
def random_manga(session: Session = Depends(get_session)):
    stmt = select(Manga).order_by(func.random()).limit(1)
    return session.exec(stmt).first()


@router.get("/trending")
def trending(session: Session = Depends(get_session), limit: int = 20):
    stmt = (
        select(
            Manga,
            func.count(Review.id).label("review_count")
        )
        .join(Review, Review.manga_id == Manga.id)
        .group_by(Manga.id)
        .order_by(func.count(Review.id).desc())
        .limit(limit)
    )

    rows = session.exec(stmt).all()

    return [
        {"manga": manga, "reviews": count}
        for manga, count in rows
    ]

@router.get("/{manga_id}")
def get_manga(manga_id: int, session: Session = Depends(get_session)):
    manga = session.get(Manga, manga_id)
    if not manga:
        return {"error": "Manga not found"}
    return manga