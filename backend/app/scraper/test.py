import asyncio
from app.scraper.crawler import fetch_best_selling_links
from app.scraper.scraper import scrape_manga_page

if __name__ == "__main__":
    dic = asyncio.run(scrape_manga_page("https://en.wikipedia.org/wiki/My_Hero_Academia"))
    print(dic)