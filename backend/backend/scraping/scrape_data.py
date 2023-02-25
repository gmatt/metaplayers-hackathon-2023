import time

import requests
from bs4 import BeautifulSoup, Tag
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

MAIN_CONTENT_CSS_SELECTOR = "div.jogszabaly"


def scrape_all_current_hungarian():
    url = ALL_HUNGARIANS_PAGE
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    last_page = int(soup.select_one(LAST_LINK_CSS_SELECTOR)["href"].split("/")[-2])

    for i in tqdm(range(1, last_page + 1), position=0):
        url = ALL_HUNGARIANS_NTH_PAGE.format(page=i)
        page = requests.get(url)

        here("../temp/index.html").write_text(page.content.decode("utf8"))
        soup = BeautifulSoup(page.content, "html.parser")
        for a in tqdm(soup.select(ITEM_LINK_CSS_SELECTOR), position=1, leave=False):
            url = SCRAPING_BASE_URL + "/" + a["href"]
            scrape_one_page_raw(url)
            time.sleep(SCRAPING_WAIT_SECONDS_BETWEEN_PAGES)
        time.sleep(SCRAPING_WAIT_SECONDS_BETWEEN_PAGES)


def scrape_one_page_raw(url: str):
    page = requests.get(url)
    outfile = here("../data/scraped/raw") / f"{url.split('/')[-1]}.html"
    text = page.content.decode("utf8")
    outfile.write_text(text)


def clean_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.select_one(MAIN_CONTENT_CSS_SELECTOR)

    # Remove footnotes.
    for sup in div.find_all("sup"):
        sup.decompose()

    # Mark hyperlinks.
    for e in div.find_all("a", class_="link"):
        if "data-jhid" in e.attrs:
            e.string = "[" + e.text + "](" + e.attrs["data-jhid"] + ")"

    # Images.
    for e in div.find_all("img"):
        e.string = "![](" + SCRAPING_BASE_URL + e.attrs["src"] + ")"

    for e in div.children:
        if type(e) is Tag:
            if "mainTitle" in e.attrs["class"]:
                e.string = "# " + e.text
            elif "jogszabalySubtitle" in e.attrs["class"]:
                e.string = "# " + e.text
            elif "hataly" in e.attrs["class"]:
                e.string = "\nHatályos: " + e.text + " -"
            elif "resz" in e.attrs["class"]:
                e.string = "## " + e.text
            elif "reszcim" in e.attrs["class"]:
                e.string = "## " + e.text
            elif "tagolo" in e.attrs["class"]:
                e.string = "### " + e.text

    text = div.text.strip()

    # Quick fixes
    text = text.replace(")  ", ") ")
    text = text.replace("§  (", "§ (")
    text = text.replace(" § (", " §\n (")
    text = text.replace("\n (", "\n - (")

    outfile = here("../data/scraped") / f"{url.split('/')[-1]}.md"

    outfile.write_text(text)


if __name__ == "__main__":
    # url = "https://njt.hu/jogszabaly/1975-1-20-24"
    # scrape_one_page_raw(url)
    scrape_all_current_hungarian()
