from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_service import retrieve_chunks, generate_answer

app = FastAPI(title="Compliance RAG API")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):

    chunks = retrieve_chunks(request.question)
    answer = generate_answer(request.question, chunks)

    return {
        "answer": answer,
        "sources": chunks
    }

@app.get("/health")
def health():
    return {"status": "ok"}
