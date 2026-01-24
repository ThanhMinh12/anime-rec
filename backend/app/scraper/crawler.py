import httpx
from bs4 import BeautifulSoup
import asyncio

BEST_SELLING_MANGA_URL = "https://en.wikipedia.org/wiki/List_of_best-selling_manga"


async def fetch_best_selling_links():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    async with httpx.AsyncClient(timeout=20, headers=headers) as client:
        resp = await client.get(BEST_SELLING_MANGA_URL)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")

    tables = soup.find_all("table", class_="wikitable")
    if not tables:
        raise RuntimeError("No wikitable found!")

    links = set()

    for table in tables:
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if not cols:
                continue

            title_cell = cols[0]
            a = title_cell.find("a")

            if not a or not a.get("href"):
                continue

            href = a["href"]

            if href.startswith("/wiki/"):
                full_url = "https://en.wikipedia.org" + href
                links.add(full_url)

            await asyncio.sleep(0.5)

    return list(links)
