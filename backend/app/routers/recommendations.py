from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import logging
import time
from ..db import get_session
from ..recs import recommend_similar
from ..cache import cache_get, cache_set
logger = logging.getLogger()
router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/{manga_id}")
def get_recommendations(manga_id: int, session: Session = Depends(get_session)):
    start = time.perf_counter()
    cache_key = f"recs:{manga_id}"
    cached = cache_get(cache_key)
    if cached:
        elapsed = (time.perf_counter() - start) * 1000
        logger.info(f"cached=true latency={elapsed:.2f}")

        return {"manga_id": manga_id, "recommendations": cached, "cached": True, "latency_ms": elapsed}
    recs = recommend_similar(manga_id, session)
    if not recs:
        elapsed = (time.perf_counter() - start) * 1000
        logger.info(f"cached=false empty=true latency_ms={elapsed:.2f}")
        return {"manga_id": manga_id, "recommendations": [], "cached": False, "latency_ms": elapsed}
    cache_set(cache_key, recs)
    elapsed = (time.perf_counter() - start) * 1000
    logger.info(f"cached=false latency_ms={elapsed:.2f}")
    return {"manga_id": manga_id, "recommendations": recs, "cached": False, "latency_ms": elapsed}
