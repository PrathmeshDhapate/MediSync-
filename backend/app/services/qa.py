from app.services.retrieval import retrieve_hybrid_chunks
import re
from app.services.retrieval import retrieve_hybrid_chunks
from app.services.generation import (
    generate_answer,
    build_citation_metadata,
)


def answer_question(question: str):
    retrieved_chunks = retrieve_hybrid_chunks(
        query=question,
        top_k=3,
    )

    if not retrieved_chunks:
        return {
            "answer": "I couldn't find relevant scientific evidence to answer this question.",
            "citations": [],
            "citation_validation": {
                "used_citations": [],
                "invalid_citations": [],
                "is_valid": True,
            },
        }

    answer = generate_answer(
        question=question,
        retrieved_chunks=retrieved_chunks,
    )

    citations = build_citation_metadata(retrieved_chunks)

    citation_validation = validate_citations(
        answer=answer,
        citations=citations,
    )

    return {
        "answer": answer,
        "citations": citations,
        "citation_validation": citation_validation,
    }

def validate_citations(answer: str, citations: list[dict]):
    matches = re.findall(r"\[S\d+(?:,\s*S\d+)*\]", answer)

    used_citations = set()

    for match in matches:
        citation_ids = match.strip("[]").split(",")

        for citation_id in citation_ids:
            used_citations.add(f"[{citation_id.strip()}]")


    valid_citations = {
        f"[{citation['citation_id']}]"
        for citation in citations
    }

    invalid_citations = used_citations - valid_citations

    return {
        "used_citations": sorted(used_citations),
        "invalid_citations": sorted(invalid_citations),
        "is_valid": len(invalid_citations) == 0,
    }