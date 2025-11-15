from sqlmodel import Session, select
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Anime, Review

def get_anime_features(session: Session):
    animes = session.exec(select(Anime)).all()
    features = []
    ids = []
    genre_set = set()
    for anime in animes:
        if anime.genres:
            genre_set.update([g.strip().lower() for g in anime.genres.split(",")])
    genre_list = sorted(genre_set)
    genre_index = {g: i for i, g in enumerate(genre_list)}


    for anime in animes:
        avg_rating = session.exec(
            select(Review.rating).where(Review.anime_id == anime.id)
        ).all()
        avg_score = np.mean(avg_rating) if avg_rating else 0.0

        year_norm = (anime.year - 1980) / 50.0 if anime.year else 0.0

        gvec = np.zeros(len(genre_list))
        if anime.genres:
            for g in anime.genres.split(","):
                g = g.strip().lower()
                if g in genre_index:
                    gvec[genre_index[g]] = 1.0

        vec = np.concatenate(([avg_score, year_norm], gvec))
        features.append(vec)
        ids.append(anime.id)

    return np.array(features), ids

def recommend_similar(anime_id: int, session: Session, top_n: int = 5):
    features, ids = get_anime_features(session)
    if anime_id not in ids:
        return []
    idx = ids.index(anime_id)
    sims = cosine_similarity([features[idx]], features)[0]
    sorted_idx = np.argsort(sims)[::-1]  # descending
    results = []
    for i in sorted_idx[1 : top_n + 1]:  # skip self
        similar_anime = session.get(Anime, ids[i])
        results.append(
            {
                "id": similar_anime.id,
                "title": similar_anime.title,
                "score": float(sims[i]),
            }
        )
    return results
