# ai/llm.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-70b-versatile"  # Free, powerful model


def load_llm():
    """
    Returns a callable function that sends a prompt to Groq
    and returns a clean text response.
    """
    client = Groq(api_key=GROQ_API_KEY)

    def generate(prompt: str) -> str:
        try:
            message = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=2048,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.choices[0].message.content.strip()

        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    return generate
