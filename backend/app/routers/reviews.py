from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from ..db import get_session
from ..models import Review, User, Anime
from ..auth import get_current_user
from ..schemas import ReviewCreate

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/")
def add_review(payload: ReviewCreate,
               session: Session = Depends(get_session),
               user=Depends(get_current_user)):
    review = Review(
        user_id=user["id"],
        anime_id=payload.anime_id,
        rating=payload.rating,
        text=payload.text
    )
    session.add(review)
    session.commit()
    session.refresh(review)
    return review

@router.get("/")
def list_reviews(session: Session = Depends(get_session)):
    return session.exec(select(Review)).all()


@router.get("/anime/{anime_id}")
def get_reviews_for_anime(anime_id: int, session: Session = Depends(get_session)):
    reviews = session.exec(select(Review).where(Review.anime_id == anime_id)).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews")
    return reviews


@router.get("/anime/{anime_id}/average-rating")
def get_average_rating(anime_id: int, session: Session = Depends(get_session)):
    avg_score = session.exec(
        select(func.avg(Review.rating)).where(Review.anime_id == anime_id)
    ).first()

    return {
        "anime_id": anime_id,
        "average_rating": float(avg_score) if avg_score is not None else None,
    }
