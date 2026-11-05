from fastapi import FastAPI

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