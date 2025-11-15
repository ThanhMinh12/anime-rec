import re, time, httpx
from bs4 import BeautifulSoup
from sqlmodel import Session
from .db import engine
from .models import Anime

BASE = "https://en.wikipedia.org"
INDEX_URL = f"{BASE}/wiki/Lists_of_anime"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_html(url: str) -> str:
    print(f"Fetching: {url}")
    resp = httpx.get(url, headers=HEADERS, timeout=60.0)
    resp.raise_for_status()
    return resp.text


def get_genre_links() -> list[str]:
    """Collect 'List of ... anime' links from the main Lists_of_anime page."""
    html = fetch_html(INDEX_URL)
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.select("a[href^='/wiki/List_of_']"):
        href = a["href"]
        text = a.get_text(strip=True)
        if "anime" in href and "List_of_anime" not in href and not href.endswith("(disambiguation)"):
            links.append((text, BASE + href))
    print(f"Found {len(links)} genre pages.")
    return links


def parse_list_page(html: str) -> list[dict]:
    """Extract anime titles and approximate years from one list page."""
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for table in soup.select("table.wikitable"):
        for row in table.select("tr")[1:]:
            cols = row.find_all("td")
            if not cols:
                continue
            title_cell = cols[0]
            title = title_cell.get_text(" ", strip=True)
            if not title:
                continue
            link = title_cell.find("a")
            wiki_url = (
                f"{BASE}{link['href']}"
                if link and link.get("href", "").startswith("/wiki/")
                else None
            )
            text = " ".join(c.get_text(" ", strip=True) for c in cols[1:])
            match = re.search(r"\b(19|20)\d{2}\b", text)
            year = int(match.group(0)) if match else None

            results.append(
                {
                    "title": title,
                    "year": year,
                    "synopsis": text[:400],
                    "wiki_url": wiki_url,
                }
            )
    print(f"  Parsed {len(results)} titles.")
    return results


def insert_anime(session: Session, data: dict):
    a = Anime(
        title=data["title"],
        synopsis=data["synopsis"],
        year=data["year"],
        image_url=None,
        author=None,
        studio=None,
        genres=None,
    )
    session.add(a)


def main():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    genre_links = get_genre_links()
    total = 0
    with Session(engine) as session:
        for name, url in genre_links:
            try:
                html = fetch_html(url)
                anime_entries = parse_list_page(html)
                for entry in anime_entries:
                    insert_anime(session, entry)
                    total += 1
                session.commit()
                print(f"✅ {len(anime_entries)} from {name}")
                time.sleep(1)  # polite delay
            except Exception as e:
                print(f"⚠️ Error at {url}: {e}")
                continue
    print(f"✅ Finished — inserted roughly {total} anime from Wikipedia.")


if __name__ == "__main__":
    main()
