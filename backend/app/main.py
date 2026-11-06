from fastapi import FastAPI
from pydantic import BaseModel,Field

from app.services.qa import answer_question

app = FastAPI(
    title="Medisync API",
    description="AI-powered disease research platform using RAG and GraphRAG",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Medisync"
    }

class ResearchQuestionRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
    )


@app.post("/api/v1/research/ask")
def ask_research_question(request: ResearchQuestionRequest):
    result = answer_question(request.question)

    return result