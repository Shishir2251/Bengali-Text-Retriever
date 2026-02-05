from fastapi import FastAPI, Query
from src.retriever import retrieve
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bengali Text Retriever")

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bengali Text Retriever API is running!"}

@app.post("/chat")
def chat(query: str = Query(..., description="Your query in Bengali")):
    """
    Query the FAISS database and get top matches.
    """
    docs = retrieve(query)
    return {"query": query, "results": docs}
