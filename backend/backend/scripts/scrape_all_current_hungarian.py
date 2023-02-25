import argparse
import os.path

from backend.scraping.scrape_data import RAW_OUTPUT_DIR, scrape_all_current_hungarian


def main():
    scrape_all_current_hungarian()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"Scrapes all current Hungarian legislations to '{os.path.normpath(RAW_OUTPUT_DIR)}'. (About "
        "35000 files.) "
    )
    args = parser.parse_args()
    main()
