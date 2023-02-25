import time

import requests
from bs4 import BeautifulSoup
from pyprojroot import here
from tqdm.auto import tqdm

SCRAPING_BASE_URL = "https://njt.hu"

SCRAPING_WAIT_SECONDS_BETWEEN_PAGES = 0.25

RAW_OUTPUT_DIR = here("../data/scraped/raw")

ALL_HUNGARIANS_PAGE = "https://njt.hu/search/-:-:-:-:1:-:-:-:-:-:-/1/50"
ALL_HUNGARIANS_NTH_PAGE = "https://njt.hu/search/-:-:-:-:1:-:-:-:-:-:-/{page}/50"
ITEM_LINK_CSS_SELECTOR = "a.now:not(.version)"
NEXT_LINK_CSS_SELECTOR = "a.next"
LAST_LINK_CSS_SELECTOR = "a.last"


def scrape_all_current_hungarian():
    url = ALL_HUNGARIANS_PAGE
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    last_page = int(soup.select_one(LAST_LINK_CSS_SELECTOR)["href"].split("/")[-2])

    for i in tqdm(range(1, last_page + 1), position=0):
        url = ALL_HUNGARIANS_NTH_PAGE.format(page=i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        for a in tqdm(soup.select(ITEM_LINK_CSS_SELECTOR), position=1, leave=False):
            url = SCRAPING_BASE_URL + "/" + a["href"]
            scrape_one_page_raw(url)
            time.sleep(SCRAPING_WAIT_SECONDS_BETWEEN_PAGES)
        time.sleep(SCRAPING_WAIT_SECONDS_BETWEEN_PAGES)


def scrape_one_page_raw(url: str):
    page = requests.get(url)
    outfile = RAW_OUTPUT_DIR / f"{url.split('/')[-1]}.html"
    text = page.content.decode("utf8")
    outfile.write_text(text)


if __name__ == "__main__":
    scrape_all_current_hungarian()
