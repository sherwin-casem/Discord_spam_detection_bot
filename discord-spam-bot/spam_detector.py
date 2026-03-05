import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def is_spam(message: str) -> bool:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a spam detector. Reply only SPAM or NOT_SPAM."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0
    )

    verdict = response.choices[0].message.content.strip()
    return verdict == "SPAM"