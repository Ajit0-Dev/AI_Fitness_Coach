# ai/llm.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")


def load_llm():
    """
    Returns a callable function that sends a prompt to Ollama
    and returns a clean text response (NO streaming).
    """

    def generate(prompt: str) -> str:
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                },
                timeout=60
            )

            response.raise_for_status()
            data = response.json()

            return data["message"]["content"].strip()

        except requests.exceptions.Timeout:
            return "⚠️ The model took too long. Try a shorter request."

        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to Ollama. Is `ollama serve` running?"

        except requests.exceptions.HTTPError as e:
            return f"⚠️ HTTP error: {e}"

        except Exception as e:
            return f"⚠️ Unexpected error: {str(e)}"

    return generate
