from openai import OpenAI
from ai.prompts import build_messages
from config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def ask_gpt(user_message: str) -> str:
    messages = build_messages(user_message)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        max_tokens=400,
    )

    return response.choices[0].message.content.strip()
