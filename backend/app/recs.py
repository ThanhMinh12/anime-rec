from sqlmodel import Session, select
from sqlalchemy import func
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Manga, Review, Genre, MangaGenre

def get_manga_features(session: Session):
    mangas = session.exec(select(Manga)).all()
    genres = session.exec(select(Genre)).all()
    manga_genres = session.exec(select(MangaGenre)).all()
    manga_to_genres = {}
    genre_index = {g.id: i for i, g in enumerate(genres)}
    for manga_gen in manga_genres:
        manga_to_genres.setdefault(manga_gen.manga_id, []).append(manga_gen.genre_id)
    rat_map = dict(
        session.exec(
            select(Review.manga_id, func.avg(Review.rating))
            .group_by(Review.manga_id)
        ).all()
    )

    features = []
    ids = []
    for manga in mangas:
        avg_score = rat_map.get(manga.id, 0)
        avg_score_norm = avg_score / 10
        year_norm = (manga.year - 1980) / 50 if manga.year else 0

        gen_vec = np.zeros(len(genres))
        for gen_id in manga_to_genres.get(manga.id, []):
            if gen_id in genre_index:
                gen_vec[genre_index[gen_id]] = 1

        vec = np.concatenate(([avg_score_norm, year_norm], gen_vec))
        features.append(vec)
        ids.append(manga.id)

    return np.array(features), ids

def recommend_similar(manga_id: int, session: Session, top_n: int = 5):
    features, ids = get_manga_features(session)
    if manga_id not in ids:
        return []
    idx = ids.index(manga_id)
    sims = cosine_similarity([features[idx]], features)[0]
    sorted_idx = np.argsort(sims)[::-1]
    results = []
    for i in sorted_idx[1 : top_n + 1]:
        similar_manga = session.get(Manga, ids[i])
        if not similar_manga:
            continue
        results.append(
            {
                "id": similar_manga.id,
                "title": similar_manga.title,
                "year": similar_manga.year,
                "score": float(sims[i]),
            }
        )
    return results
