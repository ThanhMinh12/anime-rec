import httpx
from bs4 import BeautifulSoup
import asyncio
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}

PLOT_SECTION_NAMES = [
    "plot", "synopsis", "story", "overview", "premise", "summary"
]


def extract_plot_synopsis(soup: BeautifulSoup):
    """
    Detect the Plot/Synopsis/Story heading, including:
        <h2><span class="mw-headline">Plot</span></h2>
        <div class="mw-heading"><h2 id="Plot"></h2></div>
        <h3>Story</h3>
    Then scan forward to find the FIRST <p>.
    """

    PLOT_SECTION_NAMES = ["plot", "synopsis", "story", "overview", "premise", "summary"]

    # Case 1: <h2><span class="mw-headline">Plot</span></h2>
    for header in soup.find_all(["h2", "h3"]):
        span = header.find("span", class_="mw-headline")
        if span:
            if clean_text(span.get_text()).lower() in PLOT_SECTION_NAMES:
                return first_paragraph_after(header)

    # Case 2: <div class="mw-heading"><h2 id="Plot"></h2></div>
    for div in soup.find_all("div", class_=lambda c: c and "mw-heading" in c):
        h = div.find(["h2", "h3"])
        if h:
            if clean_text(h.get_text()).lower() in PLOT_SECTION_NAMES:
                return first_paragraph_after(div)

    # Case 3: <h2 id="Plot">Plot</h2>
    for header in soup.find_all(["h2", "h3"]):
        if clean_text(header.get_text()).lower() in PLOT_SECTION_NAMES:
            return first_paragraph_after(header)

    return None



def first_paragraph_after(node):
    """
    Walk forward through ALL siblings until the FIRST <p> tag appears.
    Return its cleaned text.
    """

    sib = node.find_next_sibling()

    while sib:
        if sib.name == "p":
            text = clean_text(sib.get_text(" ", strip=True))
            if len(text) > 20:  # allow shorter paragraphs now
                return text

        # continue scanning, regardless of div / h2 / h3 / notes / whitespace
        sib = sib.find_next_sibling()

    return None


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


async def scrape_manga_page(url: str):
    await asyncio.sleep(0.4)

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(url)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    info = soup.find("table", class_="infobox")

    title_el = soup.find("h1", id="firstHeading")
    title = title_el.get_text(strip=True)

    synopsis = extract_plot_synopsis(soup)

    # ------ Extractor FIXED for Wikipedia Infobox ------
    def extract_any(*labels):
        if not info:
            return None

        for th in info.find_all("th"):  # ANY th (no class filtering)
            th_text = clean_text(th.get_text(" ", strip=True)).lower()

            for label in labels:
                if label.lower() in th_text:
                    # 1. Preferred: td.infobox-data
                    td = th.find_next_sibling("td", class_="infobox-data")
                    if td:
                        return clean_text(td.get_text(" ", strip=True))
                    # 2. Fallback: ANY td
                    td = th.find_next_sibling("td")
                    if td:
                        return clean_text(td.get_text(" ", strip=True))
        return None

    author = extract_any("Written by")
    illustrator = extract_any("Illustrated by")
    publisher = extract_any("Published by")
    magazine = extract_any("Magazine")
    genres = extract_any("Genre")

    def extract_number(raw):
        if not raw:
            return None
        m = re.search(r"\d+", raw)
        return int(m.group()) if m else None

    volumes = extract_number(extract_any("Volumes"))
    chapters = extract_number(extract_any("Chapters"))

    original_run = extract_any("Original run")
    year = None
    if original_run:
        m = re.search(r"(19|20)\d{2}", original_run)
        year = int(m.group()) if m else None

    return {
        "title": title,
        "synopsis": synopsis,
        "year": year,
        "score": None,
        "genres": genres,
        "author": author,
        "illustrator": illustrator,
        "publisher": publisher,
        "magazine": magazine,
        "volumes": volumes,
        "chapters": chapters,
    }
