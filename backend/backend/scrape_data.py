import requests
from bs4 import BeautifulSoup
from pyprojroot import here

if __name__ == "__main__":

    URL = "https://njt.hu/jogszabaly/1975-1-20-24"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    div = soup.find(class_="jogszabaly")

    text = div.text.strip()

    (
        here("../data/scraped") / f"{text.splitlines()[0].replace('/', '_per_')}.txt"
    ).write_text(text)
