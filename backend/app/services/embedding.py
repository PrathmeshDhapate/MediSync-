
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-embedding-2"
EMBEDDING_DIMENSIONS = 768


def generate_document_embedding(
    content: str,
    title: str | None = None,
) -> list[float]:

    if not content.strip():
        raise ValueError("Cannot generate embedding for empty text.")

    document = (
        f"title: {title or 'none'} | text: {content}"
    )

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=document,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )

    return response.embeddings[0].values

def generate_query_embedding(query: str) -> list[float]:
    if not query.strip():
        raise ValueError("Cannot generate embedding for an empty query.")

    formatted_query = (
        f"task: question answering | query: {query}"
    )

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=formatted_query,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )

    return response.embeddings[0].values
