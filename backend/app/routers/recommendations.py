from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session
from ..recs import recommend_similar
from ..cache import cache_get, cache_set

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/{manga_id}")
def get_recommendations(manga_id: int, session: Session = Depends(get_session)):
    cache_key = f"recs:{manga_id}"
    cached = cache_get(cache_key)
    if cached:
        return {"manga_id": manga_id, "recommendations": cached, "cached": True}
    recs = recommend_similar(manga_id, session)
    if not recs:
        raise HTTPException(status_code=404, detail="manga not found or no similar titles")
    cache_set(cache_key, recs)
    return {"manga_id": manga_id, "recommendations": recs, "cached": False}
