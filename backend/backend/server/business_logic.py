import os
import re

import requests
from dotenv import load_dotenv

from backend.answer_generation.gpt import get_gpt_completion

RETRIEVAL_API_URL = None


def create_question_for_gpt(query: str, candidate_results: list[dict]) -> str:
    candidates = "\n".join(
        "<"
        + x["meta"]["name"].replace(".txt", "")
        + "#"
        + x["meta"]["jhid"]
        + ">"
        + "\n"
        + x["content"]
        for x in candidate_results
    )

    prompt = f"""{candidates}

Az előbbi bekezdéseket is figyelembe véve válaszold meg a következő kérdést.
Amikor tudsz, helyezd el a fejezetek előtti hivatkozásokat a szövegben, például:
Példa a hivatkozás formájára: "A külföldi adózásra a <1975-1-20-24#SZ6@BE1@POA> és a <1975-1-20-24#SZ6@BE1@POB> tér ki."

Kérdés:
{query}
Válasz:
"""

    return prompt


def format_result(completion: str) -> str:
    completion = re.sub(
        "<([^>]+)>",
        "<a href='https://njt.hu/jogszabaly/\\1' class='ref-result' target='_blank'>\\1</a>",
        completion,
    )
    return completion


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
    response = response.json()
    # print(response.json())

    # Find full text for search result.
    candidates = [
        next(y for y in response["documents"] if y["id"] == x["document_id"])
        for x in response["answers"]
    ][:5]

    prompt = create_question_for_gpt(query, candidates)

    print(prompt)

    try:
        completion = get_gpt_completion(
            prompt,
            max_tokens=400,
        )
    except:
        print("There was error")
        return "Error"

    print(completion)

    completion = format_result(completion)

    return completion


if __name__ == "__main__":
    handle_request("Mit jelent az, ha a rendőr kinyújtott karjával maga felé int?")
