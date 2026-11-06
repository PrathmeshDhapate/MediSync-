from sqlalchemy import select

from app.database import SessionLocal
from app.models import PaperChunk
from app.services.embedding import generate_document_embedding

def generate_embeddings():
    with SessionLocal() as db:
        chunks = db.scalars(
            select(PaperChunk).where(
                PaperChunk.embedding.is_(None)
            )
        ).all()

        print(f"Found {len(chunks)} chunks without embeddings.")

        for chunk in chunks:
            embedding = generate_document_embedding(
                content=chunk.content,
            )

            chunk.embedding = embedding

            print(f"Generated embedding for chunk {chunk.id}")

        db.commit()
        print("Embedding generation completed!")

if __name__ == "__main__":
    generate_embeddings()