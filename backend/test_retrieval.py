
from app.services.retrieval import (
    retrieve_similar_chunks,
    retrieve_keyword_chunks,
    retrieve_hybrid_chunks,
)


def test_retrieval():
    query = "How do I cook a chocolate cake?"

    results = retrieve_similar_chunks(query, top_k=3)

    print(f"\nSemantic search: {query}")
    print(f"Retrieved {len(results)} results.\n")

    for rank, (chunk, title, distance) in enumerate(
        results,
        start=1,
    ):
        print(f"Rank: {rank}")
        print(f"Paper: {title}")
        print(f"Cosine distance: {distance:.4f}")
        print(f"Content: {chunk.content[:300]}")
        print("-" * 60)


def test_keyword_retrieval():
    query = "TREM2 Alzheimer's disease"

    results = retrieve_keyword_chunks(query, top_k=3)

    print(f"\nKeyword search: {query}")
    print(f"Retrieved {len(results)} results.\n")

    for rank, (chunk, title, score) in enumerate(
        results,
        start=1,
    ):
        print(f"Rank: {rank}")
        print(f"Paper: {title}")
        print(f"Keyword score: {score:.4f}")
        print(f"Content: {chunk.content[:300]}")
        print("-" * 60)


def test_hybrid_retrieval():
    query = "What is the population of Mars?"

    results = retrieve_hybrid_chunks(query, top_k=3)

    print(f"\nHybrid search: {query}")
    print(f"Retrieved {len(results)} results.\n")

    for rank, (chunk, title, rrf_score, semantic_distance) in enumerate(
        results,
        start=1,
    ):
        print(f"Rank: {rank}")
        print(f"Paper: {title}")
        print(f"RRF score: {rrf_score:.4f}")
        print(f"Semantic distance: {semantic_distance}")
        print(f"Content: {chunk.content[:300]}")
        print("-" * 60)


if __name__ == "__main__":
    test_retrieval()
    test_keyword_retrieval()
    test_hybrid_retrieval()
