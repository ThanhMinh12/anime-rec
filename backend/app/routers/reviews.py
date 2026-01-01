from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from ..db import get_session
from ..models import Review, User, Manga
from ..auth import get_current_user
from ..schemas import ReviewCreate

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/")
def add_review(payload: ReviewCreate,
               session: Session = Depends(get_session),
               user=Depends(get_current_user)):
    review = Review(
        user_id=user["id"],
        manga_id=payload.manga_id,
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


@router.get("/manga/{manga_id}")
def get_reviews_for_manga(manga_id: int, session: Session = Depends(get_session)):
    reviews = session.exec(select(Review).where(Review.manga_id == manga_id)).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews")
    return reviews


@router.get("/manga/{manga_id}/average-rating")
def get_average_rating(manga_id: int, session: Session = Depends(get_session)):
    avg_score = session.exec(
        select(func.avg(Review.rating)).where(Review.manga_id == manga_id)
    ).first()

    return {
        "manga_id": manga_id,
        "average_rating": float(avg_score) if avg_score is not None else None,
    }
