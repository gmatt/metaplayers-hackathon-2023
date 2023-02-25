import requests
from bs4 import BeautifulSoup
from pyprojroot import here
from tqdm.auto import tqdm

from backend.scraping.scrape_data import RAW_OUTPUT_DIR

SCRAPING_BASE_URL = "https://njt.hu"

CLEANED_OUTPUT_DIR = here("../data/scraped/cleaned")

MAIN_CONTENT_CSS_SELECTOR = "div.jogszabaly"


def scrape_one_page(url: str):
    page = requests.get(url)
    text = page.content.decode("utf8")

    text = clean_html(text)

    outfile = CLEANED_OUTPUT_DIR / f"{url.split('/')[-1]}.txt"
    outfile.write_text(text)


def clean_one_page(local_filename: str):
    text = (RAW_OUTPUT_DIR / local_filename).read_text()

    text = clean_html(text)

    outfile = CLEANED_OUTPUT_DIR / f"{local_filename.replace('.html', '')}.txt"
    outfile.write_text(text)


def clean_all():
    for file in tqdm(list(RAW_OUTPUT_DIR.glob("*"))):
        text = file.read_text()

        text = clean_html(text)

        outfile = here("../data/scraped/cleaned_all") / f"{file.stem}.txt"
        outfile.write_text(text)


def clean_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.select_one(MAIN_CONTENT_CSS_SELECTOR)

    # Remove footnotes from text.
    for e in div.find_all("sup"):
        e.decompose()

    # Add extra line breaks.
    for e in div.find_all("span", class_="jhId"):
        e.string = "\n<note>jhId=" + e["id"] + "</note>\n"
    # Beginning of paragraph should be on margin, so points under it are identifiable.
    for e in div.find_all("div", class_="bekezdesNyito"):
        if e.text[0] == " ":
            e.string = e.text[1:]

    # Save title and subtitle
    for e in div.find_all("h1", class_="jogszabalyMainTitle"):
        e.string = "<note>jogszabalyMainTitle=" + e.text + "</note>\n" + e.text
    for e in div.find_all("h2", class_="jogszabalySubtitle"):
        e.string = "<note>jogszabalySubtitle=" + e.text + "</note>\n" + e.text

    text = div.text.strip()

    return text


if __name__ == "__main__":
    pass
    # url = "https://njt.hu/jogszabaly/1975-1-20-24"
    # url = "https://njt.hu/jogszabaly/2013-5-00-00"
    # url = "https://njt.hu/jogszabaly/2013-5-00-00"
    # scrape_one_page(url)
    # clean_one_page("1999-6-20-0A.html")

    # clean_one_page("2002-35-00-00.html")
    # clean_one_page(random.choice(list(RAW_OUTPUT_DIR.glob("*"))).name)
    
    # clean_all()

