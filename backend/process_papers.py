from sqlalchemy import select

from app.database import SessionLocal
from app.models import Paper, PaperChunk

def process_papers():
    with SessionLocal() as db:
        papers = db.scalars(
            select(Paper)
        ).all()

        print(f"Found {len(papers)} papers to process.")

        for paper in papers:
            if not paper.abstract:
                print(f"Skipping paper {paper.pmid}: no abstract available.")
                continue

            content = paper.abstract.strip()
            existing_chunk = db.scalar(
                select(PaperChunk.id).where(
                    PaperChunk.paper_id == paper.id
                ).limit(1)
            )

            if existing_chunk is not None:
                print(f"Skipping paper {paper.pmid}: already processed.")
                continue

            chunk = PaperChunk(
                paper=paper,
                chunk_index=1,
                section_name="ABSTRACT",
                content=content,
            )

            db.add(chunk)

            print(f"Processed paper: {paper.pmid}")

        db.commit()
        print("Document processing completed!")

if __name__ == "__main__":
    process_papers()