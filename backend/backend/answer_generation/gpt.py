import os

import openai
from dotenv import load_dotenv


def get_gpt_completion(
    prompt: str,
    max_tokens: int = 16,
    stop=None,
) -> str:
    if not openai.api_key:
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    result = openai.Completion.create(
        model="text-davinci-003",
        # model="text-ada-001",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0,
        stop=stop,
    )
    return result["choices"][0]["text"]


if __name__ == "__main__":
    print(get_gpt_completion("I think therefore", max_tokens=3))
