from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session
from ..recs import recommend_similar
from ..cache import cache_get, cache_set

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/{anime_id}")
def get_recommendations(anime_id: int, session: Session = Depends(get_session)):
    cache_key = f"recs:{anime_id}"
    cached = cache_get(cache_key)
    if cached:
        return {"anime_id": anime_id, "recommendations": cached, "cached": True}
    recs = recommend_similar(anime_id, session)
    if not recs:
        raise HTTPException(status_code=404, detail="Anime not found or no similar titles")
    cache_set(cache_key, recs)
    return {"anime_id": anime_id, "recommendations": recs, "cached": False}
