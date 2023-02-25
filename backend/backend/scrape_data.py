import time

import requests
from bs4 import BeautifulSoup, Tag
from pyprojroot import here
from tqdm.auto import tqdm

ALL_HUNGARIANS_PAGE = "https://njt.hu/search/-:-:-:-:1:-:-:-:-:-:-/1/50"
ITEM_LINK_CSS_SELECTOR = "a.now"
NEXT_LINK_CSS_SELECTOR = "a.next"
LAST_LINK_CSS_SELECTOR = "a.last"


def scrape_all_current_hungarian():
    url = ALL_HUNGARIANS_PAGE
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    last_page = int(soup.select_one(LAST_LINK_CSS_SELECTOR)["href"].split("/")[-2])

    for i in tqdm(range(1, last_page + 1), position=0):
        url = ALL_HUNGARIANS_PAGE.replace("/1/50", f"{i}/50")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        for a in tqdm(range(10), position=1, leave=False):
            time.sleep(0.1)
        time.sleep(1)


MAIN_CONTENT_CSS_SELECTOR = "div.jogszabaly"


def scrape_one_page(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.select_one(MAIN_CONTENT_CSS_SELECTOR)

    # Remove footnotes.
    for sup in div.find_all("sup"):
        sup.decompose()

    # Mark hyperlinks.
    for e in div.find_all("a", class_="link"):
        if "data-jhid" in e.attrs:
            e.string = "[" + e.text + "](" + e.attrs["data-jhid"] + ")"

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
    url = "https://njt.hu/jogszabaly/1975-1-20-24"
    scrape_one_page(url)
