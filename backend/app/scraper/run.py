import asyncio
import random
from sqlmodel import Session, select
from app.db import engine
from app.models import Manga, Genre, MangaGenre
from app.scraper.crawler import fetch_best_selling_links
from app.scraper.scraper import scrape_manga_page, normalize_wiki_genres


# ---- RATE LIMIT ----
MAX_CONCURRENCY = 3   # scrape at most 3 pages at a time
MIN_DELAY = 1.0       # 1 sec delay between each scrape
MAX_DELAY = 1.6       # random jitter to avoid detection

semaphore = asyncio.Semaphore(MAX_CONCURRENCY)


def attach_genres(session: Session, manga_id: int, raw_genres: str):
    genre_names = normalize_wiki_genres(raw_genres)
    for name in genre_names:
        genre = session.exec(
            select(Genre).where(Genre.name == name)
        ).first()

        if not genre:
            genre = Genre(name=name)
            session.add(genre)
            session.commit()
            session.refresh(genre)

        session.refresh(
            MangaGenre(manga_id, genre.id)
        )


async def scrape_single(url, session):
    """Scrape ONE manga page with proper rate limiting."""

    async with semaphore:
        await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
        print(f"Scraping: {url}")

        try:
            data = await scrape_manga_page(url)
        except Exception as e:
            print(f"ERROR scraping {url}: {e}")
            return

        # Check if already exists
        existing = session.query(Manga).filter(Manga.title == data["title"]).first()
        if existing:
            print(f"Skipping — exists: {data['title']}")
            return

        manga = Manga(
            title=data["title"],
            synopsis=data["synopsis"],
            year=data["year"],
            score=data["score"],
            author=data["author"],
            illustrator=data["illustrator"],
            publisher=data["publisher"],
            magazine=data["magazine"],
            volumes=data["volumes"],
            chapters=data["chapters"]
        )

        session.add(manga)
        session.commit()
        session.refresh(manga)
        attach_genres(session, manga.id, data["genres"])
        session.commit()
        print(f"Saved → {data['title']}")


async def scrape_and_save_all():
    print("Fetching manga URLs…")
    urls = await fetch_best_selling_links()
    print(f"Found {len(urls)} manga pages.")

    with Session(engine) as session:
        # Schedule tasks concurrently but rate-limited
        tasks = [scrape_single(url, session) for url in urls]
        await asyncio.gather(*tasks)

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(scrape_and_save_all())
