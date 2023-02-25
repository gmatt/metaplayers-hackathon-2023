import requests
from bs4 import BeautifulSoup
from pyprojroot import here

SCRAPING_BASE_URL = "https://njt.hu"

CLEANED_OUTPUT_DIR = here("../data/scraped/cleaned")

MAIN_CONTENT_CSS_SELECTOR = "div.jogszabaly"


def scrape_one_page(url: str):
    page = requests.get(url)
    text = page.content.decode("utf8")

    text = clean_html(text)

    outfile = CLEANED_OUTPUT_DIR / f"{url.split('/')[-1]}.txt"
    outfile.write_text(text)


def clean_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.select_one(MAIN_CONTENT_CSS_SELECTOR)

    # Remove footnotes.
    for e in div.find_all("sup"):
        e.decompose()

    # Add extra line breaks.
    for e in div.find_all("span", class_="jhId"):
        e.string = "\n<note>jhId=" + e["id"] + "</note>\n"

    # Save title and subtitle
    for e in div.find_all("h1", class_="jogszabalyMainTitle"):
        e.string = "<note>jogszabalyMainTitle=" + e.text + "</note>\n" + e.text
    for e in div.find_all("h2", class_="jogszabalySubtitle"):
        e.string = "<note>jogszabalySubtitle=" + e.text + "</note>\n" + e.text

    text = div.text.strip()

    return text


if __name__ == "__main__":
    url = "https://njt.hu/jogszabaly/1975-1-20-24"
    # url = "https://njt.hu/jogszabaly/2013-5-00-00"
    scrape_one_page(url)
