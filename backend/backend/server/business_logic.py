import os

import requests
from dotenv import load_dotenv

RETRIEVAL_API_URL = None


def create_question_for_gpt():
    pass


def handle_request(query: str) -> str:
    global RETRIEVAL_API_URL
    if not RETRIEVAL_API_URL:
        load_dotenv()
        RETRIEVAL_API_URL = os.getenv("RETRIEVAL_API_URL")

    response = requests.post(
        RETRIEVAL_API_URL + "/question",
        json={"query": query},
        timeout=120,
    )

    print(response.json())
    return ""
