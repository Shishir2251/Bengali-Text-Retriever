import faiss
import pickle
import numpy as np
from src.embed_store import get_embedding

# Load FAISS index and chunks
try:
    index = faiss.read_index("db/faiss.index")
    chunks = pickle.load(open("db/chunks.pkl", "rb"))
    print("FAISS index and documents loaded successfully.")
except Exception as e:
    print("Error loading FAISS index:", e)
    index = None
    chunks = []

def retrieve(query, top_k=5):
    """
    Retrieve top_k chunks from FAISS based on query.
    Returns a list of matched text chunks.
    """
    if index is None:
        return ["Vector DB not found. Build it first!"]

    # Get embedding of query
    query_emb = get_embedding(query)  # shape (1, dim)
    
    # Search FAISS
    D, I = index.search(query_emb, top_k)  # distances and indices
    
    results = []
    for i in I[0]:
        if i < len(chunks):
            results.append(chunks[i])
    return results
