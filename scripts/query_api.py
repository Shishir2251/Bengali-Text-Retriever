from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scripts.rag_qa import retrieve_chunks, generate_answer, get_history

app = FastAPI()

class QueryRequest(BaseModel):
    user_id: str
    query: str
    lang: str  # "en" or "bn"

class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]
    grounded: bool

@app.post("/api/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    try:
        retrieved = retrieve_chunks(request.query)
        history = get_history(request.user_id)
        answer, grounded = generate_answer(request.query, retrieved, history, request.lang, request.user_id)
        sources = [{"chunk_id": f"chunk_{idx}", "score": float(score), "text": chunk[:200] + "..."} for chunk, score, idx in retrieved]  # Cast score to float
        return {"answer": answer, "sources": sources, "grounded": grounded}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))