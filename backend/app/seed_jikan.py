import httpx
from sqlmodel import Session
from .db import engine
from .models import Anime


BASE_URL = "https://api.jikan.moe/v4/anime"


def fetch_page(page: int = 1):
    """Fetch one page (25 anime by default) from Jikan."""
    print(f"Fetching page {page}...")
    with httpx.Client(timeout=60.0) as client:
        resp = client.get(BASE_URL, params={"page": page})
        resp.raise_for_status()
        return resp.json()


def insert_anime(session: Session, item: dict):
    """Insert one anime record into the database."""
    title = item.get("title") or "Unknown"
    synopsis = (item.get("synopsis") or "")[:400]
    year = item.get("year")
    image_url = item.get("images", {}).get("jpg", {}).get("large_image_url")
    score = item.get("score") or 0.0
    genres = ", ".join([g["name"] for g in item.get("genres", [])]) or None
    studios = item.get("studios", [])
    studio = studios[0]["name"] if studios else None

    anime = Anime(
        jikan_id=item["mal_id"],
        title=title,
        synopsis=synopsis,
        image_url=image_url,
        year=year,
        score=score,
        genres=genres,
        author=None,
        studio=studio,
    )
    session.add(anime)


def main():
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)

    total_inserted = 0
    with Session(engine) as session:
        for page in range(1, 6):  # Fetch first 5 pages = ~125 anime
            try:
                data = fetch_page(page)
                anime_list = data.get("data", [])
                for item in anime_list:
                    insert_anime(session, item)
                    total_inserted += 1
                session.commit()
            except Exception as e:
                print(f"⚠️ Error on page {page}: {e}")
                break
    print(f"✅ Inserted {total_inserted} anime into database from Jikan.")


if __name__ == "__main__":
    main()
