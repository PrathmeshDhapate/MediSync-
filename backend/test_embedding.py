
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Paper, PaperChunk
from app.services.embedding import generate_document_embedding


def test_embedding():
    with SessionLocal() as db:
        result = db.execute(
            select(PaperChunk, Paper.title)
            .join(Paper, PaperChunk.paper_id == Paper.id)
            .limit(1)
        ).first()

        if result is None:
            raise RuntimeError("No paper chunks found.")

        chunk, title = result

        print(f"Generating embedding for: {title}")

        embedding = generate_document_embedding(
            content=chunk.content,
            title=title,
        )

        print("Embedding generated successfully!")
        print("Dimensions:", len(embedding))
        print("First 5 values:", embedding[:5])


if __name__ == "__main__":
    test_embedding()
