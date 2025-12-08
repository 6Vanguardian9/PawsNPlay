import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

def generate_embedding(text: str) -> list[float]:
    payload = {
        "model": "mxbai-embed-large",
        "input": text
    }

    response = requests.post(f"{OLLAMA_URL}/api/embed", json=payload)
    response.raise_for_status()
    return response.json()["embedding"]