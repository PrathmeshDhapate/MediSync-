from sqlalchemy import select, func
from pgvector.sqlalchemy import Vector

from app.database import SessionLocal
from app.models import PaperChunk, Paper
from app.services.embedding import generate_query_embedding

SEMANTIC_DISTANCE_THRESHOLD = 0.35

def retrieve_similar_chunks(query: str, top_k: int = 3):
    query_embedding = generate_query_embedding(query)

    distance = PaperChunk.embedding.cosine_distance(query_embedding)

    with SessionLocal() as db:
        results = db.execute(
            select(
                PaperChunk,
                Paper.title,
                distance.label("distance"),
            )
            .join(Paper, PaperChunk.paper_id == Paper.id)
            .where(PaperChunk.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        ).all()

        return results

def retrieve_keyword_chunks(query: str, top_k: int = 3):
    search_vector = func.to_tsvector(
        "english",
        PaperChunk.content,
    )

    search_query = func.plainto_tsquery(
        "english",
        query,
    )

    rank = func.ts_rank_cd(
        search_vector,
        search_query,
    )

    with SessionLocal() as db:
        results = db.execute(
            select(
                PaperChunk,
                Paper.title,
                rank.label("rank"),
            )
            .join(Paper, PaperChunk.paper_id == Paper.id)
            .where(
                search_vector.op("@@")(search_query),
            )
            .order_by(rank.desc())
            .limit(top_k)
        ).all()

        return results

def reciprocal_rank_fusion(
    semantic_results,
    keyword_results,
    k: int = 60,
):
    fused_scores = {}
    chunk_data = {}

    for rank, result in enumerate(semantic_results, start=1):
        chunk, title, distance = result

        chunk_id = chunk.id

        if chunk_id not in fused_scores:
            fused_scores[chunk_id] = 0.0
            chunk_data[chunk_id] = {
                "chunk": chunk,
                "title": title,
                "semantic_distance": distance,
            }

        fused_scores[chunk_id] += 1 / (k + rank)

    for rank, result in enumerate(keyword_results, start=1):
        chunk, title, score = result

        chunk_id = chunk.id

        if chunk_id not in fused_scores:
            fused_scores[chunk_id] = 0.0
            chunk_data[chunk_id] = {
                "chunk": chunk,
                "title": title,
                "semantic_distance": None,
            }

        fused_scores[chunk_id] += 1 / (k + rank)

    ranked_chunks = sorted(
        fused_scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        (
            chunk_data[chunk_id]["chunk"],
            chunk_data[chunk_id]["title"],
            score,
            chunk_data[chunk_id]["semantic_distance"],
        )
        for chunk_id, score in ranked_chunks
    ]

def retrieve_hybrid_chunks(
    query: str,
    top_k: int = 3,
    candidate_k: int = 10,
):
    semantic_results = retrieve_similar_chunks(
        query,
        top_k=candidate_k,
    )

    keyword_results = retrieve_keyword_chunks(
        query,
        top_k=candidate_k,
    )

    fused_results = reciprocal_rank_fusion(
        semantic_results,
        keyword_results,
    )

    relevant_results = [
        result
        for result in fused_results
        if (
            result[3] is None
            or result[3] <= SEMANTIC_DISTANCE_THRESHOLD
        )
    ]

    return relevant_results[:top_k]