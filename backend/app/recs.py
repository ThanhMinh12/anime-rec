from sqlmodel import Session, select
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Manga, Review

def get_manga_features(session: Session):
    mangas = session.exec(select(Manga)).all()
    features = []
    ids = []
    genre_set = set()
    for manga in mangas:
        if manga.genres:
            genre_set.update([g.strip().lower() for g in manga.genres.split(",")])
    genre_list = sorted(genre_set)
    genre_index = {g: i for i, g in enumerate(genre_list)}


    for manga in mangas:
        avg_rating = session.exec(
            select(Review.rating).where(Review.manga_id == manga.id)
        ).all()
        avg_score = np.mean(avg_rating) if avg_rating else 0.0

        year_norm = (manga.year - 1980) / 50.0 if manga.year else 0.0

        gvec = np.zeros(len(genre_list))
        if manga.genres:
            for g in manga.genres.split(","):
                g = g.strip().lower()
                if g in genre_index:
                    gvec[genre_index[g]] = 1.0

        vec = np.concatenate(([avg_score, year_norm], gvec))
        features.append(vec)
        ids.append(manga.id)

    return np.array(features), ids

def recommend_similar(manga_id: int, session: Session, top_n: int = 5):
    features, ids = get_manga_features(session)
    if manga_id not in ids:
        return []
    idx = ids.index(manga_id)
    sims = cosine_similarity([features[idx]], features)[0]
    sorted_idx = np.argsort(sims)[::-1]  # descending
    results = []
    for i in sorted_idx[1 : top_n + 1]:  # skip self
        similar_manga = session.get(Manga, ids[i])
        results.append(
            {
                "id": similar_manga.id,
                "title": similar_manga.title,
                "score": float(sims[i]),
            }
        )
    return results
