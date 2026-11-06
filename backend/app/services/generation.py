from google import genai
from google.genai import types
import os
from pathlib import Path

from dotenv import load_dotenv

from app.prompts.answer_prompt import ANSWER_PROMPT

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)

def build_context(retrieved_chunks):
    context_parts = []

    for index, (chunk, title, rrf_score,semantic_distance) in enumerate(
        retrieved_chunks,
        start=1,
    ):
        context_part = f"""
Citation ID: [S{index}]
Paper ID: {chunk.paper_id}
Chunk ID: {chunk.id}
Paper Title: {title}

Scientific Evidence:
{chunk.content}
"""
        context_parts.append(context_part)

    return "\n\n---\n\n".join(context_parts)

def generate_answer(question: str, retrieved_chunks):
    context = build_context(retrieved_chunks)

    prompt = ANSWER_PROMPT.format(
        question=question,
        context=context,
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        ),
    )

    return response.text

def build_citation_metadata(retrieved_chunks):
    citations = []

    for index, (chunk, title, rrf_score,semantic_distance) in enumerate(
        retrieved_chunks,
        start=1,
    ):
        citations.append({
            "citation_id": f"S{index}",
            "paper_id": chunk.paper_id,
            "chunk_id": chunk.id,
            "paper_title": title,
        })

    return citations