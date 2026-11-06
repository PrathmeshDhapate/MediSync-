from app.database import SessionLocal
from app.models import Paper, PaperChunk

with SessionLocal() as db:
    paper = db.query(Paper).filter(
        Paper.pmid == "10196523"
    ).first()

    if paper is None:
        print("Paper not found!")
    else:
        print("Paper found:", paper.title)
        chunk = PaperChunk(
            paper=paper,
            chunk_index=1,
            section_name="ABSTRACT",
            content="Alzheimer's disease is associated with amyloid-beta and tau pathology.",
            token_count=12,
        )

        chunk = db.query(PaperChunk).filter(
            PaperChunk.paper_id == paper.id,
            PaperChunk.chunk_index == 1,
        ).first()

        if chunk:
            print("Chunk found:", chunk.content)
            print("Original paper:", chunk.paper.title)
